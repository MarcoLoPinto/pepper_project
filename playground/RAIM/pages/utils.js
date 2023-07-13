class Routing {
    constructor(startingPage) {
        // Get a reference to the body element
        const body = document.querySelector('body');
        // Get an array of all the div elements that are direct children of the body element
        const divs = Array.from(body.querySelectorAll('div'));
        // Filter the divs array to only include elements that have a parent of the body element
        const bodyDivs = divs.filter(div => div.parentNode === body);
        // Extract the IDs of the body divs into a new array
        this.routes = bodyDivs.map(div => div.id);

        this.goToPage(startingPage);
    }
    goToPage(page) {
        for (let p of this.routes) {
            let element = document.getElementById(p);
            element.style.display = 'none';
        }
        let element = document.getElementById(page);
        element.style.display = 'block';
    }

}

class SpeechRecognitionBrowser {
    constructor(lang) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList;
        const SpeechRecognitionEvent = window.SpeechRecognitionEvent || window.webkitSpeechRecognitionEvent;

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = lang || "en-US";

        this.synthesis = window.speechSynthesis;

        this.recognition.onspeechend = () => {
            this.recognition.stop();
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    startListening() {
        return new Promise((resolve, reject) => {
            this.recognition.start();
            this.recognition.onresult = async (event) => {
                const transcript = event.results[0][0].transcript;
                this.stopListening();
                await this.sleep(200);
                resolve(transcript);
            };
            this.recognition.onerror = (event) => {
                reject(event.error);
            };
        });
    }

    restartListening() {
        this.recognition.restart();
    }

    stopListening() {
        this.recognition.stop();
    }

    speak(text, onEnd) {
        const utterance = new SpeechSynthesisUtterance(text);
        this.synthesis.speak(utterance);
        utterance.onend(onEnd)
    }

}

class LanguageText {
    constructor(lang, textMapping) {
        this.lang = lang;
        this.textMapping = textMapping;
        this.defaultlang = "en-US";
    }
    get(name) {
        if (!(name in this.textMapping)) throw `${name} not present in the vocabulary!`
        if (!(this.lang in this.textMapping[name])) throw `${this.lang} not present in the ${name} vocabulary!`
        return this.textMapping[name][this.lang];
    }
}