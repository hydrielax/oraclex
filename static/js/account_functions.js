
String.prototype.slugify = function (separator = "-") {
    return this
        .toString()
        .normalize('NFD')                   // split an accented letter in the base letter and the acent
        .replace(/[\u0300-\u036f]/g, '')   // remove all previously split accents
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9 ]/g, '')   // remove all chars not letters, numbers and spaces (to be replaced)
        .replace(/\s+/g, separator);
}

function create_username() {
    input = document.getElementById('id_username');
    if (input.value == "") {
        first_name = document.getElementById('id_first_name').value[0].toLowerCase();
        last_name = document.getElementById('id_last_name').value.slugify('-');
        input.value = first_name + last_name;
    }
}