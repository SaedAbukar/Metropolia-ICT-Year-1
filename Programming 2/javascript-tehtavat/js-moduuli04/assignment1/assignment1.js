const form = document.querySelector('form');
form.addEventListener('submit', async function(evt) {
  evt.preventDefault();
  const tvShow = document.querySelector('input[name=q]').value;
  try {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${tvShow}`);
    const jsonData = await response.json();
    console.log(jsonData)
  } catch (error) {
    console.log(error.message);
  }
});