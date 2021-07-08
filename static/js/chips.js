
var input = document.querySelector(".chip-input");
var chips = document.querySelector(".chips-set");

/*
input.onfocus = function () {
    motscles.style.display = 'block';
    input.style.borderRadius = "5px 5px 0 0";  
  };
  for (let option of motscles.options) {
    option.onclick = function () {
      input.value = option.value;
      motscles.style.display = 'none';
      input.style.borderRadius = "5px";
    }
  };
*/
  
document.querySelector(".form-field")
.addEventListener('click',() => {
    //input.style.display = 'block';
    input.focus();
});

input.addEventListener('blur',()=>{
    //input.style.display = 'none';
});

input.addEventListener('keypress', function(event) {
    if(event.which === 13){
        chips.appendChild(function () {
            var _chip = document.createElement('div');
            _chip.classList.add('chips-group');
            _chip.classList.add('chip');
            //_chip.addEventListener('click', chipClickHandler);
            _chip.append(
                (function () {
                    var _chip_text = document.createElement('span');
                    _chip_text.classList.add('chips');
                    _chip_text.classList.add('chips-label');
                    _chip_text.innerHTML = input.value;
                    return _chip_text;
                })(),
                (function () {
                    var _chip_button = document.createElement('button');
                    _chip_button.classList.add('chips');
                    _chip_button.classList.add('chips-btn');
                    _chip_button.classList.add('chips-only-icon');
                    _chip_button.innerHTML = '<i class="icons-close" aria-hidden="true"></i>';
                    _chip_button.addEventListener('click', chipClickHandler);
                    return _chip_button;
                })()
            );
            return _chip;
        }());
        input.value = '';
    }
});

function chipClickHandler(event){
    chips.removeChild(event.currentTarget.parentNode);
}