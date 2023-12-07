const map = L.map('map').setView([60.23, 24.74],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: 'blue-icon'});
const greenIcon = L.divIcon({className: 'green-icon'});

const startingPointIcon = L.icon({
    iconUrl: '../icons/starting_point.png', // Replace with the path to your icon image
    iconSize: [41, 41], // Size of the icon. This is the default size for Leaflet's marker icon.
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location.
    popupAnchor: [8, -41] // Point from which the popup should open relative to the iconAnchor.
});

document.addEventListener('DOMContentLoaded', async (e) => {

    const fields = await getFields();
    const opponents = await getOpponents();
    const currentField =  await setStartingField();
    console.log(fields);
    console.log(opponents);
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

// function kelvinToCelcius(kelvin){
//     return Math.floor(kelvin - 273.15);
// }


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
    if (!currentField) {
    console.error("Current field is undefined");
    return; // or handle the error appropriately
    }
    const lat = currentField.latitude_deg;
    const lon = currentField.longitude_deg;
    const response = await fetch(`http://127.0.0.1:3000/fields/closest/${lat}/${lon}`);
    const fields = await response.json();

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
    return fields;
}

async function travelToAirport(airport, co2_emissions, dist){
    const conf = confirm(`Do you want to travel to ${airport.name}`);

    if(conf) {
        distance += dist;
        co2_consumed += co2_emissions;

        distanceElement.innerText = `${distance}KM`;
        CO2Element.innerText = `${Math.floor(co2_consumed)}KG`;

        airportMarkers.clearLayers();

        const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {'icon': startingPointIcon}).
            addTo(map).
            bindPopup(airport.name).
            openPopup();
        airportMarkers.addLayer(marker);

        map.flyTo([airport.latitude_deg, airport.longitude_deg]);

        await getClosestAirports(airport);
        // await showQuestion();
        // await getCurrentAirportWeather(airport);
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





// Search by ICAO ******************************
// const searchForm = document.querySelector('#single');
// const input = document.querySelector('input[name=icao]');
// searchForm.addEventListener('submit', async function(evt) {
//   evt.preventDefault();
//   const icao = input.value;
//   const response = await fetch('http://127.0.0.1:3000/get_field_info/' + icao);
//   const airport = await response.json();
//   // remove possible other markers
//   airportMarkers.clearLayers();
//   // add marker
//   const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).
//       addTo(map).
//       bindPopup(airport.name).
//       openPopup();
//   airportMarkers.addLayer(marker);
//   // pan map to selected airport
//   map.flyTo([airport.latitude_deg, airport.longitude_deg]);
// });
// **********************************************

// Choose from list *****************************
// const continentList = document.querySelector('#continents');
// const countryList = document.querySelector('#countries');
// const airportList = document.querySelector('#airports');
//
// // Start with adding continents
// async function showContinents() {
//   const response = await fetch('http://127.0.0.1:3000/continents');
//   const continents = await response.json();
//   for (const cont of continents) {
//     const option = document.createElement('option');
//     option.value = cont.continent;
//     option.innerText = cont.continent;
//     continentList.appendChild(option);
//   }
// }
//
// showContinents(); // this starts the loading of continents
//
// // when continent is selected get countries and add to second list...
// continentList.addEventListener('change', async function() {
//   countryList.innerHTML = '<option>Select Country</option>'; // empty the country and airport lists because the user might change continent
//   airportList.innerHTML = '<option>Select Airport</option>';
//   const response = await fetch(
//       'http://127.0.0.1:3000/wc_fields/' + continentList.value);
//   const countries = await response.json();
//   for (const country of countries) {
//     const option = document.createElement('option');
//     option.value = country.iso_country;
//     option.innerText = country.name;
//     countryList.appendChild(option);
//   }
// });
//
// // when country is selected get airports and add to third list...
// countryList.addEventListener('change', async function() {
//   airportList.innerHTML = '<option>Select Airport</option>'; // empty the airport list because the user might change country
//   const response = await fetch(
//       'http://127.0.0.1:3000/airports/' + countryList.value);
//   const airports = await response.json();
//   for (const airport of airports) {
//     const option = document.createElement('option');
//     option.value = airport.ident;
//     option.innerText = airport.name;
//     airportList.appendChild(option);
//   }
// });
//
// // when airport is selected show it on the map...
// airportList.addEventListener('change', async function() {
//   const response = await fetch(
//       'http://127.0.0.1:3000/airport/' + airportList.value);
//   const airport = await response.json();
//   // remove possible other markers
//   airportMarkers.clearLayers();
//   // add marker
//   const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).
//       addTo(map).
//       bindPopup(airport.name).
//       openPopup();
//   airportMarkers.addLayer(marker);
//   // pan map to selected airport
//   map.flyTo([airport.latitude_deg, airport.longitude_deg]);
// });
//
// // *********************************************

