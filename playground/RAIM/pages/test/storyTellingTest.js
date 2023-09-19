const story_card_container = document.getElementById('card-container');
const prp_title = document.getElementById("prp_title")
const pepper_feedback = {
    default: function() {return},
    hear: function() {return},
    no_hear: function() {return},
    speak: function() {return},
    invisible: function() {return},
    visible: function() {return},
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
        "PEPPER_NO_HEAR": {
            "en-US": "I didn't hear your response, please speak up",
            "it-IT": "Non ho sentito la tua risposta, per favore alza la voce"
        },
        "PEPPER_STORY_OVER_AGE": {
            "en-US": "You said to be %s, so maybe you're too young for %s",
            "it-IT": "Hai detto di avere %s anni, quindi forse sei troppo piccolo per %s"
        },
        "PEPPER_CHOOSE_STORY": {
            "en-US": "Choose a story among those",
            "it-IT": "Scegli una storia tra queste"
        },
        "PEPPER_CONFIRM_STORY": {
            "en-US": "So the story is %s?",
            "it-IT": "Quindi la storia è %s?"
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
        "PEPPER_ACTION_CHOSEN_BY_PEPPER": {
            "en-US": "I'll select an action for you",
            "it-IT": "Sceglierò io una azione al tuo posto"
        },
        "PEPPER_STORY_FINISHED": {
            "en-US": "What an amazing story, so fun and personal! Did you like it?",
            "it-IT": "Che storia fantastica, cosi divertente e personale! Ti è piaciuta?"
        },
        "PEPPER_STORY_LIKED": {
            "en-US": "I'm glad to hear it! See you for the next one. Goodbye!",
            "it-IT": "Sono felice di sentirlo! Alla prossima storia. Ciao!"
        },
        "PEPPER_STORY_NOT_LIKED": {
            "en-US": "I'm sorry you didn't like it. I hope the next one will be better. Goodbye!",
            "it-IT": "Mi dispiace non ti sia piaciuta. Spero la prossima sia migliore. Ciao!"
        },
        "PEPPER_STORY_LIKED_NO_HEAR": {
            "en-US": "I couldn't understand your response. I still hope the story was good. Goodbye!",
            "it-IT": "Non ho capito la tua risposta. Comunque spero la storia ti sia piaciuta. Ciao!"
        }
    }
);
var storyTellingManager = new StoryTellingManager({lang})

const self = {
    languageText,
    storyTellingManager,
    // pepper: new PepperClient({
    //     onConnect: async () => {
    //         try {
    //             await self.pepper.stand(true);
    //             console.log("Pepper connected.");
    //         }
    //         catch(error) {
    //             console.error("Something went wrong on the pepper server");
    //         }
    //     }
    // }),
    pepper: {
        sayMove: function(txt){
            console.log("PEPPER SAYS: " + txt)
            return self.sleep(500)
        }
    },
    console,
    stt: {
        startListening: window.readStt
    },
    sleep: function(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    // Story card functions
    addCardToContainer: function(content) {
        let card = document.createElement("labels");
        card.classList.add("card");
        card.innerText = content;
        story_card_container.appendChild(card);
    },
    clearContainer: function() {
        story_card_container.innerHTML = "";
    },
    setCardAsUnselected: function(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
    },
    setCardAsSelected: function(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
        cards[index].classList.add("card-chosen");
    },
    setCardAsConfirmed: function(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.remove("card-chosen", "card-chosen-confirmation");
        cards[index].classList.add("card-chosen-confirmation");
    },
    setCardAsOverage: function(index) {
        let cards = story_card_container.querySelectorAll(".card");
        cards[index].classList.add("card-overage");
    },
    toggleCardAsSelected: function(index){
        cards = story_card_container.querySelectorAll(".card")
        cards[index].classList.toggle("card-chosen")
    },
    toggleCardAsConfirmed: function( index){
        cards = story_card_container.querySelectorAll(".card")
        cards[index].classList.toggle("card-chosen-confirmation")
    },

    splitTextIntoChunks: function(text) {
        const MIN_LENGTH = 50;
        const punctuationRegex = /([,.])/g;
        const chunks = text.split(punctuationRegex);
        const result = [];
        const concatenatedResult = [];
        let addToLastSentence = false;
    
        for (let i = 0; i < chunks.length; i += 2) {
            const chunk = chunks[i].trim();
            const punctuation = chunks[i + 1] || '';
    
            if (chunk) {
                result.push(chunk + punctuation);
            }
        }
    
        for(let r of result) {
            if(r.length < MIN_LENGTH && concatenatedResult.length > 0 && r[r.length-1] == ",") concatenatedResult[concatenatedResult.length-1] += " " + r;
            else concatenatedResult.push(r);
        }
    
        return concatenatedResult;
    },
    
    sayMoveLongText: async function(prompt, mood, html_text_element) {
        html_text_element.innerText = prompt;
        let prompts = self.splitTextIntoChunks(prompt);
    
        for(let p of prompts){
            await self.pepper.sayMove(
                p,
                mood,
                true
            );
        }
    }
}

async function storyGame() {
    self.storyTellingManager.reset();
    self.clearContainer();
    // self.routing.goToPage("prp_page");
    self.console.log("Selecting story!");
    let storyNameChosen = await selectStory();
    if (storyNameChosen !== false) {
        self.console.log("Starting story!");
        let jobExecuted = await startStory(storyNameChosen);
        if (jobExecuted !== false) {
            self.console.log("Ending story!");
            // Story finished
            let txt = self.languageText.get("PEPPER_STORY_FINISHED");
            prp_title.innerText = txt;
            pepper_feedback.speak();
            await self.pepper.sayMove(
                txt,
                PepperClient.MOVE_NAMES.excited,
                true
            );

            try {
                pepper_feedback.hear();
                let confirm_text = await self.stt.startListening();
                if (confirm_text.toLowerCase() == self.languageText.get("YES").toLowerCase()) {
                    let txt = self.languageText.get("PEPPER_STORY_LIKED");
                    prp_title.innerText = txt
                    pepper_feedback.speak();
                    await self.pepper.sayMove(
                        txt,
                        PepperClient.MOVE_NAMES.excited,
                        true
                    );
                    pepper_feedback.default();
                }
                else if (confirm_text.toLowerCase() == self.languageText.get("NO").toLowerCase()) {
                    let txt = self.languageText.get("PEPPER_STORY_NOT_LIKED");
                    prp_title.innerText = txt
                    pepper_feedback.speak();
                    await self.pepper.sayMove(
                        txt,
                        PepperClient.MOVE_NAMES.excited,
                        true
                    );
                    pepper_feedback.default();
                }
                else {
                    let txt = self.languageText.get("PEPPER_STORY_LIKED_NO_HEAR");
                    prp_title.innerText = txt
                    pepper_feedback.no_hear();
                    await self.pepper.sayMove(
                        txt,
                        PepperClient.MOVE_NAMES.excited,
                        true
                    );
                    pepper_feedback.default();
                }
            } catch (error) {
                self.console.error(error);
                let txt = self.languageText.get("PEPPER_STORY_LIKED_NO_HEAR");
                label_explanation.innerText = txt;
                pepper_feedback.no_hear();
                await self.pepper.sayMove(
                    txt,
                    PepperClient.MOVE_NAMES.kisses,
                    true
                );
                self.sleep(1000);
                pepper_feedback.default();
            }
        } else {
            self.console.error("Error during story");
        }
    }
    // self.routing.goToPage("index_page"); 
}

async function selectStory() {
    // Gathering the list of available stories
    let stories = [];
    let storiesOverage = [];
    let storiesLower = [];
    let user = {age:12}
    try {
        stories = await self.storyTellingManager.listStories();
        storiesOverage = await self.storyTellingManager.listStoriesOverage(user.age || 150); // 150 years old to say that there is no age limit
        storiesLower = stories.map((s) => s.toLowerCase());
    } catch (error) {
        self.console.log("Error in gathering stories:", error);
        return false;
    }
    // Displaying them
    for (let i in stories) {
        let storyName = stories[i];
        self.addCardToContainer(storyName);
        if (storiesOverage.includes(storyName)) {
            self.setCardAsOverage(i)
        }
    }
    //Saying the overage stories
    if (storiesOverage.length > 0) {
        storiesOverageStr = storiesOverage.join(", ")
        let txt = self.languageText.get("PEPPER_STORY_OVER_AGE").replace('%s', user.age).replace('%s', storiesOverageStr);
        prp_title.innerText = txt;
        pepper_feedback.speak();
        await self.pepper.sayMove(
            txt,
            PepperClient.MOVE_NAMES.thinking,
            true
        );
        pepper_feedback.default();
    }
    // Choose the story loop
    let storyChosen = -1;
    while (storyChosen == -1) {
        try {
            // Pepper asks to user which stories to select and the user responds
            prp_title.innerText = self.languageText.get("PEPPER_CHOOSE_STORY");
            pepper_feedback.speak();
            await self.pepper.sayMove(
                self.languageText.get("PEPPER_CHOOSE_STORY"),
                PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                true
            );
            pepper_feedback.hear();
            let selectedStoryNameLower = (await self.stt.startListening()).toLowerCase();
            // If the story selected is one of the proposed...
            if (storiesLower.includes(selectedStoryNameLower)) {
                let selectedStoryIndex = storiesLower.indexOf(selectedStoryNameLower);
                let selectedStoryName = stories[selectedStoryIndex];
                self.setCardAsSelected(selectedStoryIndex);
                // Pepper asks if the story selected is the correct one
                let confirmationQuestion = self.languageText.get("PEPPER_CONFIRM_STORY").replace('%s', selectedStoryName);
                prp_title.innerText = confirmationQuestion;
                pepper_feedback.speak();
                await self.pepper.sayMove(
                    confirmationQuestion,
                    PepperClient.MOVE_NAMES.fancyRightArmCircle,
                    true
                );
                pepper_feedback.hear();
                let confirmationResponse = await self.stt.startListening();
                // Checking the YES/NO response
                if (confirmationResponse.toLowerCase() == self.languageText.get("YES").toLowerCase()) {
                    self.setCardAsConfirmed(selectedStoryIndex);
                    pepper_feedback.speak();
                    await self.pepper.sayMove(
                        self.languageText.get("PEPPER_START_STORY"),
                        PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                        true
                    );
                    pepper_feedback.default();
                    storyChosen = selectedStoryIndex;
                }
                else {
                    pepper_feedback.default();
                    self.setCardAsUnselected(selectedStoryIndex);
                }
            }
            // ...otherwise:
            else {
                let notUnderstoodQuestion = self.languageText.get("PEPPER_STORY_NOT_UNDERSTOOD").replace('%s', selectedStoryNameLower);
                prp_title.innerText = notUnderstoodQuestion;
                pepper_feedback.speak();
                await self.pepper.sayMove(
                    notUnderstoodQuestion,
                    PepperClient.MOVE_NAMES.confused,
                    true
                );
                pepper_feedback.default();
            }
        }
        // If the robot does not hear
        catch (error) {
            self.console.log("An error occurred (propbably no response)");
            self.console.error(error);
            prp_title.innerText = self.languageText.get("PEPPER_NO_HEAR");
            pepper_feedback.no_hear();
            await self.pepper.sayMove(
                self.languageText.get("PEPPER_NO_HEAR"),
                PepperClient.MOVE_NAMES.fancyRightArmCircle,
                true
            );
            await self.sleep(1000); // TODO: check if necessary on tablet
            pepper_feedback.default();
        }

    }

    let storyNameChosen = stories[storyChosen];
    return storyNameChosen;
}

async function startStory(storyNameChosen) {
    // Starting the story
    try {
        await self.storyTellingManager.startStory(storyNameChosen);
    } catch (error) {
        self.console.error("Error in starting the story:", error);
        return false;
    }
    self.console.log("Starting story loop...");
    // Story Loop
    while (!self.storyTellingManager.storyFinished) {
        self.clearContainer();
        let { newPrompts, newMoods, nextActions } = await self.storyTellingManager.getNewPromptsAndActions()
            .catch(() => {
                self.console.log("Error in gathering new prompts:", error);
                return false;
            });
        for (let i = 0; i < newPrompts.length; i++) {
            let prompt = newPrompts[i];
            let mood = newMoods[i];

            pepper_feedback.speak();
            await self.sayMoveLongText(prompt, mood, prp_title);
            await self.sleep(200);
            pepper_feedback.default();
        }
        // If the story is finished, exit!
        if (self.storyTellingManager.storyFinished) break;
        // Show the new actions to the user:
        for (let i = 0; i < nextActions.length; i++) {
            let actionPretext = nextActions[i];
            self.addCardToContainer(`${i + 1}: ${actionPretext}`);
        }

        // Choose action loop:
        let actionChosen = -1;
        let maxRepeatCount = 3;
        let repeatCount = 0;
        while (actionChosen == -1) {
            try {
                // Pepper asks to user which action to select and the user responds
                let txt = self.languageText.get("PEPPER_CHOOSE_STORY_ACTION");
                prp_title.innerText = txt;
                pepper_feedback.speak();
                await self.pepper.sayMove(
                    txt,
                    PepperClient.MOVE_NAMES.bothArmsBumpInFront,
                    true
                );
                pepper_feedback.hear();
                let selectedActionIndexStr = (await self.stt.startListening()).toLowerCase();
                let selectedActionIndex = Number(selectedActionIndexStr) - 1;
                // If the action selected is one of the proposed...
                if (selectedActionIndex <= nextActions.length) {
                    self.setCardAsSelected(selectedActionIndex);
                    // Pepper asks if the action selected is the correct one
                    let confirmationQuestion = self.languageText.get("PEPPER_CONFIRM_STORY_ACTION").replace('%s', selectedActionIndexStr);
                    prp_title.innerText = confirmationQuestion;
                    pepper_feedback.speak();
                    await self.pepper.sayMove(
                        confirmationQuestion,
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    pepper_feedback.hear();
                    let confirmationResponse = await self.stt.startListening();
                    // Checking the YES/NO response
                    if (confirmationResponse.toLowerCase() == self.languageText.get("YES").toLowerCase()) {
                        actionChosen = selectedActionIndex;
                    }
                    else {
                        self.setCardAsUnselected(selectedActionIndex);
                    }
                }
                // ...otherwise:
                else {
                    let notUnderstoodQuestion = self.languageText.get("PEPPER_ACTION_INDEX_NOT_UNDERSTOOD").replace('%s', selectedActionIndexStr)
                    prp_title.innerText = notUnderstoodQuestion;
                    pepper_feedback.no_hear();
                    await self.pepper.sayMove(
                        notUnderstoodQuestion,
                        PepperClient.MOVE_NAMES.confused,
                        true
                    );
                    pepper_feedback.default();
                }
            }
            // If the robot does not hear
            catch (error) {
                self.console.log("An error occurred (propbably no response)");
                self.console.error(error);
                prp_title.innerText = self.languageText.get("PEPPER_NO_HEAR");
                pepper_feedback.no_hear();
                await self.pepper.sayMove(
                    self.languageText.get("PEPPER_NO_HEAR"),
                    PepperClient.MOVE_NAMES.fancyRightArmCircle,
                    true
                );
                pepper_feedback.default();

                // Counting how many times the user didn't respond
                repeatCount++;
                if (repeatCount > maxRepeatCount) {
                    actionChosen = 0;

                    prp_title.innerText = self.languageText.get("PEPPER_ACTION_CHOSEN_BY_PEPPER");
                    pepper_feedback.speak();
                    await self.pepper.sayMove(
                        self.languageText.get("PEPPER_ACTION_CHOSEN_BY_PEPPER"),
                        PepperClient.MOVE_NAMES.fancyRightArmCircle,
                        true
                    );
                    pepper_feedback.default();
                }
                else {
                    await self.sleep(1000); // TODO: check if necessary on tablet
                }
            }

        }
        // Action selected, go on...
        self.setCardAsConfirmed(actionChosen);
        await self.storyTellingManager.executeAction(actionChosen);
    }

    return true;
}

setTimeout(()=>storyGame(),500)