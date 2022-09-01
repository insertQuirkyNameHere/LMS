const dataList = document.querySelector('#authorsList')
const authInp = document.querySelector('#authors')
const optionsEle = document.querySelectorAll('#authorsList option')
let optionsList = []
let inpCommas = 0
for (let i of optionsEle){
    optionsList.push(i.value)
}
console.log(optionsList)

function updateDatalist(prefix){
    dataList.innerHTML = "";
    for(let option of optionsList){
        let newOptionEle = document.createElement('option');
        newOptionEle.textContent = prefix + ', ' + option.value;
        dataList.appendChild(newOptionEle);
    }
}
authInp.addEventListener('keyup', function(){
    console.log('here')
    let trimmedInp = authInp.value.trim();
    let numOfCommas = trimmedInp.match(/,/g).length;
    let posOfLastComma = trimmedInp.lastIndexOf(',');
    let prefix = trimmedInp.substring(0, posOfLastComma)
    console.log('Prefix:', prefix);
    console.log('Trimmed Inp:', trimmedInp);
    console.log('Num of Commas', numOfCommas);
    if(numOfCommas > inpCommas){
        print('Input commas: ', numOfCommas)
        updateDatalist(prefix)
    }
    inpCommas = numOfCommas
})