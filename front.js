const port = "5000"
const libraryUrl = "http://localhost:" + port + "/";
fetch(libraryUrl)
  .then((response) => response.json())
  .then((allBooksInfos) => display(allBooksInfos));


function display(allBooksInfos) {
  library = document.getElementById("library");
  library.innerHTML = "";
  allBooksInfos.map((bookInfo) => {
    book = create_book(bookInfo);
    library.appendChild(book);
  });
}

function create_book(bookInfo) {
  let {book, id, available, title, author, category, price, image, imageMenuWrapper, add, remove} = createDivs()

  addClasses(book, id, available, title, author, category, price, image, imageMenuWrapper, add, remove)
  insertContent(bookInfo, id, available, title, author, category, price, image, add, remove)
  appendElements(book, available, title, author, category, price, imageMenuWrapper, id)
  appendElements(imageMenuWrapper, image, add, remove)

  let bookID = bookInfo[0]

  bindContext(add, bookID)
  bindContext(remove, bookID)

  add.onclick = add_quantity;
  remove.onclick = delete_quantity;

  return book;
}

function createDivs(bookInfo){
  let book = newDiv('div');
  let id = newDiv('span');
  let available = newDiv('span');
  let title = newDiv('span');
  let author = newDiv('span');
  let category = newDiv('span');
  let price =newDiv('span');
  let image = newDiv('img');
  let imageMenuWrapper = newDiv('div');
  let add = newDiv('p');
  let remove = newDiv('p');

  return {book, id, available, title, author, category, price, image, imageMenuWrapper, add, remove}
}

function newDiv(element){
  return document.createElement(element)
}

function addClasses(book, id, available, title, author, category, price, image, imageMenuWrapper, add, remove){
  book.classList.add("book");
  id.classList.add("id");
  available.classList.add("available");
  title.classList.add("title");
  author.classList.add("author");
  category.classList.add("category");
  price.classList.add("price");
  image.classList.add("image");
  imageMenuWrapper.classList.add("imageMenuWrapper");
  add.classList.add("add");
  remove.classList.add("remove");
}

function insertContent(bookInfo, id, available, title, author, category, price, image, add, remove){
  id.innerText = bookInfo[0];
  available.innerText = bookInfo[1] + " available";
  title.innerText = bookInfo[2];
  author.innerText = bookInfo[3];
  category.innerText = bookInfo[4];
  price.innerText = "$" + bookInfo[5];
  image.src = bookInfo[6];
  add.innerText = "➕";
  remove.innerText = "➖";
}

function appendElements(father, ...elements){
  elements.map(
    (element)=>{father.appendChild(element)}
  )
}

function bindContext(button, context) {
  button.context = context;
}

function add_quantity() {
  let bookID = this.context;
  const incrementBookURL = libraryUrl + "/increment/" + bookID;
  fetch(incrementBookURL)
    .then((response) => response.json())
    .then((allBooksInfos) => display(allBooksInfos));
}

function delete_quantity() {
  let bookID = this.context;
  const decrementBookURL = libraryUrl + "/decrement/" + bookID;
  fetch(decrementBookURL)
    .then((response) => response.json())
    .then((allBooksInfos) => display(allBooksInfos));
}

function addBook() {
  let bookInfo = getBookInfo();

  const addBookUrl = libraryUrl + "add/";

  fetch(addBookUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bookInfo),
  })
    .then((res) => res.json())
    .then((allBooksInfos) => display(allBooksInfos));

    refreshAddInputs()
}

function getBookInfo(){
  let bookInfo = {
    available: document.getElementById("availableInput").value,
    title: document.getElementById("titleInput").value,
    author: document.getElementById("authorInput").value,
    category: document.getElementById("categoryInput").value,
    price: document.getElementById("priceInput").value,
    url: document.getElementById("urlInput").value,
  };

  return bookInfo;

}
function refreshAddInputs(){
  document.getElementById("availableInput").value = ""
  document.getElementById("titleInput").value = ""
  document.getElementById("authorInput").value = ""
  document.getElementById("categoryInput").value = ""
  document.getElementById("priceInput").value = ""
  document.getElementById("urlInput").value = ""
}

function searchBook(){
    let bookName = document.getElementById("searchBookInput").value
    const searchBookURL = libraryUrl + "/search/" + bookName;
    fetch(searchBookURL)
    .then((response) => response.json())
    .then((allBooksInfos) => display(allBooksInfos));
    document.getElementById("searchBookInput").value = ""
}

function showBooks(){
    fetch(libraryUrl)
  .then((response) => response.json())
  .then((allBooksInfos) => display(allBooksInfos));
}

