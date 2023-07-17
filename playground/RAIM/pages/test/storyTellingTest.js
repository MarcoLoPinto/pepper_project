const story_card_container = document.getElementById('card-container');
const prp_title = document.getElementById("prp_title")



function addCardToContainer(content){
    let card = document.createElement("labels")
    card.classList.add("card")
    card.innerText = content
    story_card_container.appendChild(card)
}

function clearContainer(){
    story_card_container.innerHTML = ""
}

function toggleCardAsSelected(index){
    cards = story_card_container.querySelectorAll(".card")
    cards[index].classList.toggle("card-chosen")
}

function toggleCardAsConfirmed( index){
    cards = story_card_container.querySelectorAll(".card")
    cards[index].classList.toggle("card-chosen-confirmation")
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
        },
        "PEPPER_CHOOSE_STORY_ACTION": {
            "en-US": "How do you want to proceed? Tell me the action number",
            "it-IT": "Come vuoi precedere? Dimmi il numero dell'azione"
        },
        "PEPPER_CONFIRM_STORY_ACTION": {
            "en-US": "So the next step is the action number %s?",
            "it-IT": "Quindi il prossimo passo è l'azione numero %s?"
        },
        "PEPPER_ACTION_INDEX_NOT_UNDERSTOOD": {
            "en-US": "%s is not one of the possible selectable actions, maybe i got it wrong, can you repeat?",
            "it-IT": "%s non è una delle azioni che puoi selezionare, forse ho capito male, puoi ripetere?"
        },
        "PEPPER_STORY_FINISHED": {
            "en-US": "What an amazing story, so fun and personal! Well. Goodbye",
            "it-IT": "Che storia fantastica, cosi divertente e personale! Beh. Arrivederci"
        }
    }
);

const self = {
    languageText,
    storyTellingManager: new StoryTellingManager({lang: "en-US"}),
    pepper: new PepperClient({
        onConnect: async () => {
            try {
                await self.pepper.stand(true);
                console.log("Pepper connected.");
            }
            catch(error) {
                console.error("Something went wrong on the pepper server");
            }
        }
    }),
    console
}

async function storyGame() {
    // this.routing.goToPage("prp_page");

    self.storyTellingManager.reset()
    clearContainer()

    // Story selection
    try {
        let stories = await self.storyTellingManager.listStories()
        let storiesLower = stories.map((s) => s.toLowerCase())

        for(let i in stories){
            let storyName = stories[i]
            addCardToContainer(storyName)
        }
        
        
        let storyChosen = -1
        prp_title.innerText = self.languageText.get("PEPPER_CHOOSE_STORY")
        await self.pepper.sayMove(
            self.languageText.get("PEPPER_CHOOSE_STORY"), 
            PepperClient.MOVE_NAMES.bothArmsBumpInFront,
            true
        );
        while (storyChosen == -1) {
            
            // let story_name_text = await this.stt.startListening().toLowerCase();
            let selectedStoryNameLower = (await readStt()).toLowerCase()

            if(storiesLower.includes(selectedStoryNameLower)){
                let selectedStoryIndex = storiesLower.indexOf(selectedStoryNameLower)
                let selectedStoryName = stories[selectedStoryIndex]
                toggleCardAsSelected(selectedStoryIndex)
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
                    toggleCardAsSelected(selectedStoryIndex)
                    prp_title.innerText = self.languageText.get("PEPPER_CHOOSE_STORY")
                    await self.pepper.sayMove(
                        self.languageText.get("PEPPER_CHOOSE_STORY"), 
                        PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                        true
                    );
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
            }
        }

        toggleCardAsConfirmed(storyChosen)
        let storyNameChosen = stories[storyChosen]
        await self.storyTellingManager.startStory(storyNameChosen)

        // Story Loop
        while(!self.storyTellingManager.storyFinished){
            clearContainer()
            let {newPrompts, newMoods, nextActions} = await self.storyTellingManager.getNewPromptsAndActions()
            for (let i = 0; i < newPrompts.length; i++) {
                let prompt = newPrompts[i];
                let mood = newMoods[i];

                prp_title.innerText = prompt
                await self.pepper.sayMove(
                    prompt, 
                    mood,
                    true
                );
                await sleep(prompt.length * 50);
            }

            if(self.storyTellingManager.storyFinished) break;

            for (let i = 0; i < nextActions.length; i++) {
                let actionPretext = nextActions[i];
                addCardToContainer(`${i+1}: ${actionPretext}`)
            }

            let actionChosen = -1
            let txt = self.languageText.get("PEPPER_CHOOSE_STORY_ACTION")
            prp_title.innerText = txt
            await self.pepper.sayMove(
                txt, 
                PepperClient.MOVE_NAMES.fancyRightArmCircle,
                true
            );
            while (actionChosen == -1) {
                
                // let selectedActionIndexStr = await this.stt.startListening();
                let selectedActionIndexStr = (await readStt()).toLowerCase()
                let selectedActionIndex = Number(selectedActionIndexStr)-1

                if (selectedActionIndex <= nextActions.length){
                    toggleCardAsSelected(selectedActionIndex)

                    txt = self.languageText.get("PEPPER_CONFIRM_STORY_ACTION").replace('%s', selectedActionIndexStr)
                    prp_title.innerText = txt
                    await self.pepper.sayMove(
                        txt, 
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    
                    // let confirmationResponse = await this.stt.startListening();
                    let confirmationResponse = await readStt()

                    if (confirmationResponse.toLowerCase() == self.languageText.get("YES").toLowerCase()) {
                        // await self.pepper.sayMove(
                        //     self.languageText.get("PEPPER_START_STORY"), 
                        //     PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                        //     true
                        // );
                        actionChosen = selectedActionIndex
                    }
                    else {
                        toggleCardAsSelected(selectedActionIndex)
                        let txt = self.languageText.get("PEPPER_CHOOSE_STORY_ACTION")
                        prp_title.innerText = txt
                        await self.pepper.sayMove(
                            txt, 
                            PepperClient.MOVE_NAMES.fancyRightArmCircle,
                            true
                        );
                    }
                }
                else {
                    notUnderstoodQuestion = self.languageText.get("PEPPER_ACTION_INDEX_NOT_UNDERSTOOD").replace('%s', selectedActionIndexStr)
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
            
            toggleCardAsConfirmed(actionChosen)
            await self.storyTellingManager.executeAction(actionChosen)
        }


        // Story finished, say goodbye
        let txt = self.languageText.get("PEPPER_STORY_FINISHED")
        prp_title.innerText = txt
        await self.pepper.sayMove(
            txt, 
            PepperClient.MOVE_NAMES.kisses,
            true
        );
        
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