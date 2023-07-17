const story_card_container = document.getElementById('card-container');
const prp_title = document.getElementById("prp_title")



function addCardToContainer(container, content){
    let card = document.createElement("labels")
    card.classList.add("card")
    card.innerText = content
    container.appendChild(card)
}

function toggleCardAsSelected(container, index){
    cards = container.querySelectorAll(".card")
    cards[index].classList.toggle("card-chosen")
}

var lang = "en-US"
var languageText = new LanguageText(
    lang, 
    {
        "YES": {
            "en-US": "yes",
            "it-IT": "si"
        },
        "NO": {
            "en-US": "no",
            "it-IT": "no"
        },
        "DETECT_NEW_FACES": {
            "en-US": "I'm detecting new faces!",
            "it-IT": "Vedo delle possibili facce nuove!"
        },
        "PEPPER_WHAT_IS_FACE_NAME": {
            "en-US": "What is the name of this person?",
            "it-IT": "Qual'è il nome di questa persona?"
        },
        "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION": {
            "en-US": "So the name is %s, correct?",
            "it-IT": "Quindi il nome è %s, corretto?"
        },
        "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION_YES": {
            "en-US": "Ok, I'm saving the name then",
            "it-IT": "Ok, allora mi salvo il nome"
        },
        "PEPPER_WHAT_IS_FACE_NAME_CONFIRMATION_NO": {
            "en-US": "The name is not correct? Let's retry",
            "it-IT": "Non è corretto? Allora riproviamo"
        },
        "PEPPER_NO_HEAR": {
            "en-US": "I didn't hear your response, please speak up",
            "it-IT": "Non ho sentito la tua risposta, per favore alza la voce"
        },
        "PEPPER_LOST_CHOSEN_ONE": {
            "en-US": "Oh no, I lost you. Come back whenever you want!",
            "it-IT": "Oh no, ti ho perso di vista. Ritorna quando vuoi!"
        },
        "PEPPER_EXPERT_USER_INTRO": {
            "en-US": "Welcome back %s! Do you want me to explain the game again?",
            "it-IT": "Ciao di nuovo %s! Vuoi che ti spieghi di nuovo il gioco?"
        },
        "PEPPER_NEW_USER_INTRO": {
            "en-US": "Hello %s! My name is PepperTale! Do you want an explanation of the game?",
            "it-IT": "Piacere di conoscerti %s! Vuoi che ti spieghi come funziona il gioco?"
        },
        "PEPPER_CHOOSE_STORY": {
            "en-US": "Choose a story among those",
            "it-IT": "Scegli una storia tra queste"
        },
        "PEPPER_CONFIRM_STORY": {
            "en-US": "So the chosen story is %s?",
            "it-IT": "Quindi la storia scelta è %s?"
        },
        "PEPPER_STORY_NOT_UNDERSTOOD": {
            "en-US": "%s is not one of the available stories, maybe i got it wrong, can you repeat please?",
            "it-IT": "%s non è tra le storie disponibili, forse ho capito male, puoi ripetere per favore?"
        },
        "PEPPER_START_STORY": {
            "en-US": "Ok, let's begin!",
            "it-IT": "Ok, iniziamo!"
        }
    }
);

const self = {
    languageText,
    storyTellingManager: new StoryTellingManager(),
    pepper: new PepperClient({
        onConnect: async () => {
            try {
                await this.pepper.stand(true);
                this.console.log("Pepper connected.");
            }
            catch(error) {
                this.console.error("Something went wrong on the pepper server");
            }
        }
    }),
    console
}

async function storyGame() {
    // this.routing.goToPage("prp_page");

    self.storyTellingManager.reset()

    // "PEPPER_CHOOSE_STORY"
    // "PEPPER_CONFIRM_STORY"
    // "PEPPER_STORY_NOT_UNDERSTOOD"
    // "PEPPER_START_STORY"

    // //Story selection
    try {
        let stories = await self.storyTellingManager.listStories()
        let storiesLower = stories.map((s) => s.toLowerCase())

        for(let i in stories){
            let storyName = stories[i]
            addCardToContainer(story_card_container, storyName)
        }
        
        let storyChosen = -1
        while (storyChosen == -1) {
            prp_title.innerText = self.languageText.get("PEPPER_CHOOSE_STORY")
            await self.pepper.sayMove(
                self.languageText.get("PEPPER_CHOOSE_STORY"), 
                PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                true
            );
            // let story_name_text = await this.stt.startListening().toLowerCase();
            let selectedStoryNameLower = (await readStt()).toLowerCase()

            if(storiesLower.includes(selectedStoryNameLower)){
                let selectedStoryIndex = storiesLower.indexOf(selectedStoryNameLower)
                let selectedStoryName = stories[selectedStoryIndex]
                toggleCardAsSelected(story_card_container, selectedStoryIndex)
                let confirmationQuestion = self.languageText.get("PEPPER_CONFIRM_STORY").replace('%s', selectedStoryName)
                prp_title.innerText = confirmationQuestion
                await self.pepper.sayMove(
                    confirmationQuestion, 
                    PepperClient.MOVE_NAMES.fancyRightArmCircle,
                    true
                );

                // let confirmationResponse = await this.stt.startListening();
                let confirmationResponse = await readStt()

                if (confirmationResponse.toLowerCase() == self.languageText.get("YES").toLowerCase()) {
                    await self.pepper.sayMove(
                        self.languageText.get("PEPPER_START_STORY"), 
                        PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                        true
                    );
                    storyChosen = selectedStoryIndex
                }
                else {
                    toggleCardAsSelected(story_card_container, selectedStoryIndex)
                }
            }
            else {
                notUnderstoodQuestion = self.languageText.get("PEPPER_STORY_NOT_UNDERSTOOD").replace('%s', selectedStoryNameLower)
                prp_title.innerText = notUnderstoodQuestion
                await self.pepper.sayMove(
                    notUnderstoodQuestion, 
                    PepperClient.MOVE_NAMES.confused,
                    true
                );

                // DEBUG
                await sleep(2000)
            }
        }





        
        

    // Story loop
        
    } catch (error) {
        self.console.log("An error occurred (propbably no response)");
        self.console.error(error);
        // prp_title.innerText = this.languageText.get("PEPPER_NO_HEAR");
        // await this.pepper.sayMove(
        //     this.languageText.get("PEPPER_NO_HEAR"), 
        //     PepperClient.MOVE_NAMES.fancyRightArmCircle,
        //     true
        // );
        // await this.sleep(1000);
        // this.storyGame();
    }
}

setTimeout(()=>storyGame(),250)