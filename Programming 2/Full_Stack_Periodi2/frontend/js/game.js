'use strict';

const map = L.map('map').setView([60.23, 24.74],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);


// Getting and creating the necessary elements for the game

const airportMarkers = L.featureGroup().addTo(map);
const visitedFields = [];

const blueIcon = L.divIcon({className: 'blue-icon'});
const greenIcon = L.divIcon({className: 'green-icon'});

const stageElement = document.querySelector('.stats-stage-target');
const CO2Element = document.querySelector('.stats-co2-target');
const distanceElement = document.querySelector('.stats-distance-target');
const travelTimesElement = document.querySelector('.stats-travel-target');
const MAP = document.querySelector('.map-stats');
const oppStatus = document.querySelector('.opponent-status');

let playerName;
let co2_consumed = 0;
let distance = 0;
let travelTimes = 0;

const startingPointIcon = L.icon({
    iconUrl: '../icons/beligol.jpg', // Replace with the path to your icon image
    iconSize: [61, 61], // Size of the icon. This is the default size for Leaflet's marker icon.
    iconAnchor: [25, 38], // Point of the icon which will correspond to marker's location.
    popupAnchor: [8, -41] // Point from which the popup should open relative to the iconAnchor.
});

document.addEventListener('DOMContentLoaded', async (e) => {
    penaltyImg.classList.add('hide')
    startButton.classList.add('hide');
    p1.classList.add('hide');
    // p2.classList.remove('hide');

    const fieldsBase = await getFields();
    const opponentsBase = await getOpponents();


    const currentField =  await setStartingField();
    // console.log(fields);
    // console.log(opponents);
    console.log(currentField);
    // const closestFields = await getClosestFields();
    // console.log(closestFields);

    // await showStartingFields(fields);
    await getCurrentFieldWeather(currentField);
    await getClosestFields(currentField);

    // console.log(fields);
    // console.log(opponents);
    // console.log(current_airport);
    // console.log(closestFields);
});


// Getting the fields from the database through api
async function getFields() {
  const response = await fetch('http://127.0.0.1:3000/get_fields');
  const fields = await response.json();

  return fields;
}


// Setting starting fields for every game
async function setStartingField() {
    const options = ['CBCP', 'CROG', 'MMEA', 'MMEB', 'MMEJ', 'KAHS', 'KATT', 'KCLF', 'KFPB', 'KHRS', 'KLFF', 'KLSS', 'KMBS', 'KMLS', 'KNRG', 'KSFS'];
    const random_icao = options[Math.floor(Math.random() * options.length)];

    airportMarkers.clearLayers();

    const response = await fetch('http://127.0.0.1:3000/fields/' + random_icao);
    const airport = await response.json();

    const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {'icon': startingPointIcon}).
        addTo(map).
        bindPopup(airport.name).
        openPopup();
    airportMarkers.addLayer(marker);

    // pan map to selected airport
    map.flyTo([airport.latitude_deg, airport.longitude_deg]);

    return airport;
}

// Getting the closest fields for the user
async function getClosestFields(currentField){
    if (visitedFields.some(item => item === currentField)) {
        console.log(visitedFields);
        console.log('The object is in the array');
    }
    if (!currentField) {
    console.error("Current field is undefined");
    return; // or handle the error appropriately
    }
    const lat = currentField.latitude_deg;
    const lon = currentField.longitude_deg;
    const response = await fetch(`http://127.0.0.1:3000/fields/closest/${lat}/${lon}`);
    const fields = await response.json();


    // Assigning the opponents randomly to 7 different field
    function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
    const opponents = await getOpponents();

    // Shuffle the opponents array
    const shuffledOpponents = shuffleArray([...opponents]);

    const numberOfFieldsToAssign = 7;

    for (let i = 0; i < numberOfFieldsToAssign && i < shuffledOpponents.length; i++) {
        fields[i].opponent = shuffledOpponents[i];
}

    for (const field of fields) {
        if (currentField.name !== field.name){
            const co2_emissions = calculateCO2(field.Distance_KM);
            const distance = Math.floor(field.Distance_KM);7

            // for (const visited of visitedFields) {
            //
            // }

            const marker = L.marker([field.latitude_deg, field.longitude_deg])
                .addTo(map)
                .bindPopup(`
                            <div id="travelPopup">
                                <h3>${field.name}</h3>
                                <button class="airport-btn" data-airport-name="${field.name}">Travel to field</button>                            
                                <p>Distance: ${distance}KM</p>
                                <p>CO2 consumption: ${co2_emissions}KG</p>
                                <div class="dropdown-confirm">
                                    <div class="confirm-content">
                                        <p>Confirm travel?</p>
                                        <button class="confirm-btn">Yes</button>
                                        <button class="cancel-btn">No</button>
                                    </div>
                                </div>
                            </div>`);
            marker.on('popupopen', function (event) {
                setTimeout(() => { // Timeout to ensure the popup's DOM is ready
                    document.querySelectorAll('.airport-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            document.querySelector('.dropdown-confirm').style.display = 'block';
                        });

                        document.querySelector('.confirm-btn').addEventListener('click', function() {
                            // Handle confirm action
                            marker.closePopup();

                            document.querySelector('.dropdown-confirm').style.display = 'none';
                            travelToAirport(field, co2_emissions, distance, true);
                        });

                        document.querySelector('.cancel-btn').addEventListener('click', function() {
                            // Handle cancel action
                            document.querySelector('.dropdown-confirm').style.display = 'none';
                            marker.closePopup();
                        });

                    });
                }, 1);
            });

            // marker.on('popupopen', function (event) {
            //     setTimeout(() => { // Timeout to ensure the popup's DOM is ready
            //         document.querySelectorAll('.airport-btn').forEach(button => {
            //             button.addEventListener('click', function () {
            //                 travelToAirport(field, co2_emissions, distance);
            //             });
            //         });
            //     }, 1);
            // });
            airportMarkers.addLayer(marker);
        }
    }
    console.log(fields);
    return fields;
}


// Moving the user to the demanded field
async function travelToAirport(field, co2_emissions, dist, conf){
    if (visitedFields.includes(field)) {
        alert(`You have already visited this field. Travel to another field!`)
    } else {
    // const conf = confirm(`Do you want to travel to ${field.name}`);

    if(conf) {
        visitedFields.push(field);
        console.log(visitedFields);
        distance += dist;
        co2_consumed += co2_emissions;
        travelTimes++
        console.log(co2_consumed);
        console.log(distance);
        console.log(travelTimes);

        distanceElement.innerText = `${distance}KM`;
        CO2Element.innerText = `${Math.floor(co2_consumed)}KG`;
        travelTimesElement.innerText = `${travelTimes}`;

        airportMarkers.clearLayers();

        const marker = L.marker([field.latitude_deg, field.longitude_deg], {'icon': startingPointIcon}).
            addTo(map).
            bindPopup(field.name).
            openPopup();
        airportMarkers.addLayer(marker);

        map.flyTo([field.latitude_deg, field.longitude_deg]);

        await getClosestFields(field);
        await getCurrentFieldWeather(field);
        console.log(field);

        // Checking if the field has an opponent and starting the penalty-shootout game if there's an opponent
        if (field.hasOwnProperty('opponent')) {
            oppStatus.innerHTML = `You found an opponent! Get ready for the match against ${field.opponent['name']}!`
            penaltyImg.classList.remove('hide')
            penStartDiv.classList.remove('hide');
            startButton.classList.remove('hide');
            p1.classList.remove('hide');
            MAP.style.display = 'none';
            // p2.classList.add('hide');
            penaltyImg.classList.remove('hide')
            startButton.classList.remove('hide');
            p1.classList.remove('hide');
            // p2.classList.add('hide');
        }else{
            oppStatus.innerHTML = `There was no opponent in this field. Continue the search and travel to next field... `;
        }
    }}
}


// Calculating the co2 emissions for each flight
function calculateCO2(distance) {
    const fuel_burn_per_hour = 500;
    const cruising_speed_km_hr = 900;

    const co2_per_gallon_fuel = 9.57;
    const fuel_burn_per_km = fuel_burn_per_hour / cruising_speed_km_hr;

    const co2_emissions = distance * fuel_burn_per_km * co2_per_gallon_fuel

    return Math.floor(co2_emissions)
}

// Getting the opponents from the database through api
async function getOpponents() {
  const response = await fetch('http://127.0.0.1:3000/get_opponents');
  const opponents = await response.json();

  return opponents
}

async function updateLocation(icao, p_range, u_points, g_id) {
  const response = await fetch(`http://127.0.0.1:3000/update_location/${icao}/${p_range}/${u_points}/${g_id}`)
}

const tempElement = document.querySelector('.weather-temp-target');
const weatherImgElement = document.querySelector('.weather-icon-target');


// Getting current weather for the current field
async function getCurrentFieldWeather(current_airport) {
    const api_key = '6ce33329d9eb56fcde8cc14e07aa160e';

    const lat = current_airport.latitude_deg;
    const lon = current_airport.longitude_deg;

    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${api_key}`);
    const weather = await response.json();

    const icon = weather.weather[0].icon;
    const temp = `${kelvinToCelcius(weather.main.temp)}°C`;

    tempElement.innerText = temp;
    weatherImgElement.src = `https://openweathermap.org/img/wn/${icon}.png`;
}


// Converting kelvins to celsius.
function kelvinToCelcius(kelvin){
    return Math.floor(kelvin - 273.15);
}
