const MEMORY_NAME = "state_machine"

let initMemory = {
    
};

function getMemory() {
    const storedObj = JSON.parse(localStorage.getItem(MEMORY_NAME));
    return storedObj;
}

function setMemory(value) {
    localStorage.setItem(MEMORY_NAME, JSON.stringify(obj));
}