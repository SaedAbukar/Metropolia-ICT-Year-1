const map = L.map('map').setView([60.23, 24.74],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const airportMarkers = L.featureGroup().addTo(map);
const visitedFields = [];

const blueIcon = L.divIcon({className: 'blue-icon'});
const greenIcon = L.divIcon({className: 'green-icon'});

const stageElement = document.querySelector('.stats-stage-target');
const CO2Element = document.querySelector('.stats-co2-target');
const distanceElement = document.querySelector('.stats-distance-target');
const travelTimesElement = document.querySelector('.stats-travel-target');
const MAP = document.querySelector('.map');

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
    // await getCurrentAirportWeather(current_airport);
    await getClosestFields(currentField);

    // console.log(fields);
    // console.log(opponents);
    // console.log(current_airport);
    // console.log(closestFields);
});


async function getFields() {
  const response = await fetch('http://127.0.0.1:3000/get_fields');
  const fields = await response.json();

  return fields;
}



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

// async function showStartingFields(fields) {
//
//   for (const field of fields) {
//
//     const marker = L.marker([field.latitude_deg, field.longitude_deg]).
//         addTo(map).
//         bindPopup(field.name).
//         openPopup();
//     airportMarkers.addLayer(marker);
//   }
//
//   map.flyTo([fields[0].latitude_deg, fields[0].longitude_deg]);
//
// }


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
            const distance = Math.floor(field.Distance_KM);

            const marker = L.marker([field.latitude_deg, field.longitude_deg])
                .addTo(map)
                .bindPopup(`
                            <div>
                                <h3>${field.name}</h3>
                                <button class="airport-btn" data-airport-name="${field.name}">Travel to field</button>                            
                                <p>Distance: ${distance}KM</p>
                                <p>CO2 consumption: ${co2_emissions}KG</p>
                            </div>`);

            marker.on('popupopen', function (event) {
                setTimeout(() => { // Timeout to ensure the popup's DOM is ready
                    document.querySelectorAll('.airport-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            travelToAirport(field, co2_emissions, distance);
                        });
                    });
                }, 1);
            });
            airportMarkers.addLayer(marker);
        }
    }
    console.log(fields);
    return fields;
}

async function travelToAirport(field, co2_emissions, dist){
    const conf = confirm(`Do you want to travel to ${field.name}`);

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
        if (field.hasOwnProperty('opponent')) {
            const oppConf = confirm(`You found an opponent! Get ready for the match against ${field.opponent['name']}!`)
            if (oppConf) {
                penaltyImg.classList.remove('hide')
                penStartDiv.classList.remove('hide');
                startButton.classList.remove('hide');
                p1.classList.remove('hide');
                // Map.classList.add('hide');
                // p2.classList.add('hide');
            }else{
            const oppConf2 = confirm(`Stop fooling around and get ready for the game! If you are scared then just close the tap and call it a day...`);
            penaltyImg.classList.remove('hide')
            startButton.classList.remove('hide');
            p1.classList.remove('hide');
            // p2.classList.add('hide');
            }
        }else{
            alert(`There was no opponent in this field. Continue the search and travel to next field... `);
        }
    }
}

function calculateCO2(distance) {
    const fuel_burn_per_hour = 500;
    const cruising_speed_km_hr = 900;

    const co2_per_gallon_fuel = 9.57;
    const fuel_burn_per_km = fuel_burn_per_hour / cruising_speed_km_hr;

    const co2_emissions = distance * fuel_burn_per_km * co2_per_gallon_fuel

    return Math.floor(co2_emissions)
}


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
async function getCurrentFieldWeather(current_airport) {
    const api_key = 'f806590ff13e2499734e34a745c8ee63';

    const lat = current_airport.latitude_deg;
    const lon = current_airport.longitude_deg;

    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${api_key}`);
    const weather = await response.json();

    const icon = weather.weather[0].icon;
    const temp = `${kelvinToCelcius(weather.main.temp)}°C`;

    tempElement.innerText = temp;
    weatherImgElement.src = `https://openweathermap.org/img/wn/${icon}.png`;
}

function kelvinToCelcius(kelvin){
    return Math.floor(kelvin - 273.15);
}
