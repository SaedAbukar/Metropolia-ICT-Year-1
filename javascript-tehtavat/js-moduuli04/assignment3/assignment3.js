const form = document.querySelector('form');

form.addEventListener('submit', async function(evt) {
  evt.preventDefault();
  const tvShow = document.querySelector('input[name=q]').value;
  try {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${tvShow}`);
    const jsonData = await response.json();
    if (jsonData.length > 0) {
      const showData = jsonData[0].show;
      const showName = showData.name;
      const officialSite = showData.url;
      const image = showData.image?.medium;
      const summary = showData.summary;
      result(showName, officialSite, image, summary);
    } else {
      console.log("No shows found");
    }
  } catch (error) {
    console.log(error.message);
  }
});

function result(showName, officialSite, image, summary) {

  const existingContainer = document.getElementById("results");
  if (existingContainer) {
    existingContainer.innerHTML = '';
  }
  const headerTwo = document.createElement('h2');
  const div = document.createElement('div');
  const a = document.createElement('a');
  const img = document.createElement('img');
  const article = document.createElement('article');
  const elementContainer = document.createElement('div');

  headerTwo.textContent = showName;
  div.innerHTML = summary;
  a.href = officialSite
  a.innerHTML = showName;
  a.target = "_blank";
  img.src = image;
  img.alt = showName;
  article.append(headerTwo, a, img, div);
  // console.log(a);
  // console.log(headerTwo);
  // console.log(div);
  // console.log(img);
  // console.log(article);
  elementContainer.id = "results";
  elementContainer.append(article);

  document.body.appendChild(elementContainer);
}