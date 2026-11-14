document.querySelector('#add_item').addEventListener('click', function () {
  const item = document.createElement('li');
  item.textContent = 'Item';
  document.querySelector('ul.my_list').appendChild(item);
});
