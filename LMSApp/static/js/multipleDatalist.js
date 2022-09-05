const authDataList = document.querySelector('#authorsList');
const authInp = document.querySelector('#authors');
const optionsEle = document.querySelectorAll('#authorsList option');

const genreInp = document.querySelector('#genre');
const genreDataList = document.querySelector('#genreList');
const genreOptionsEle = document.querySelectorAll('#genreList option');

let authOptionsList = [];
for (let i of optionsEle){
    authOptionsList.push(i.value);
}

let genreOptionsList = [];
for (let i of genreOptionsEle){
    genreOptionsList.push(i.value);
}

authInp.addEventListener('keyup', function(){
    let inpText = authInp.value;
    prefix = generatePrefix(inpText);
    updateDataList(prefix, authDataList, authOptionsList);
})

genreInp.addEventListener('keyup', function(){
    let inpText = genreInp.value;
    prefix = generatePrefix(inpText);
    updateDataList(prefix, genreDataList, genreOptionsList);
})


function updateDataList(prefix, dataList, optionsList){
    dataList.innerHTML = '';
    for (let i of optionsList){
        let newOption = document.createElement('option');
        newOption.textContent = prefix + ', ' + i;
        if (newOption.textContent[0] === ','){
            newOption.textContent = newOption.textContent.substring(2, newOption.textContent.length);
        }
        dataList.appendChild(newOption);
    }
}

function generatePrefix(inpText){
    inpText.trim();
    let authorList = inpText.split(',');
    authorList = authorList.slice(0, authorList.length-1);
    prefix = authorList.join(',');
    return prefix;
}