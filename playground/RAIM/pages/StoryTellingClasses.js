class StoryTellingClient {
    
    static StoryAction = class {
        constructor(type, properties = {}){
            this.type = type
            this.properties = properties
        }
        
        toServerObj(){
            return { 
                "action_type": this.type,
                "action_properties": this.properties
            }
        }
    }

    static MOVE_NAMES = {
        bothArmsBumpInFront: "bothArmsBumpInFront", 
        fancyRightArmCircle: "fancyRightArmCircle", 
        normalPosture: "normalPosture"
    };
    static EYE_PARTS = {Both:"Both", Left:"Left", Right:"Right"}

    constructor({receiveListener = (command) => {}, onConnect = () => {}, onDisconnect = () => {}}){
        // RAIM Client
        this.RAIMClient = new RAIMClient("storytellingclient");
        this.RAIMClient.debug = false;
        this.RAIMClient.setCommandListener(receiveListener);
        this.RAIMClient.onDisconnect = onDisconnect;
        
        this.RAIMClient.connect(...RAIMgetWebsocketUrlParams()).then(onConnect);
    }

    sendAction(action, request = true) {
        let command_in = new RAIMClient.Command({
            data: {
                "actions": [action.toServerObj()]
            },
            to_client_id: "story_telling",
            request: request,
        });
        return this.RAIMClient.dispatchCommand(command_in)
    }

    quit(){
        let action = new StoryTellingClient.StoryAction("quit")
        return this.sendAction(action, false);
    }

    listStories(request = true){
        let action = new StoryTellingClient.StoryAction("story_list")
        return this.sendAction(action, request);
    }

    startStory(name, lang, request = true){
        let action = new StoryTellingClient.StoryAction("story_start",{
            story_name: name,
            story_language: lang
        })
        return this.sendAction(action, request);
    }

    getStoryUntilNow(id, request = true){
        let action = new StoryTellingClient.StoryAction("story_until_now",{
            story_id: id
        })
        return this.sendAction(action, request);
    }

    executeAction(id, actionIndex, request = true){
        let action = new StoryTellingClient.StoryAction("story_execute_action",{
            story_id: id,
            story_action_index: actionIndex
        })
        return this.sendAction(action, request);
    }

}

class StoryTellingManager {

    constructor({lang = "EN", onConnect = () => {}}){
        this.client = StoryTellingClient({onConnect})
        this.lang = lang
        this.storyId = null
        this.promptIndex = 0
        this.storyFinished = false
        this.nextActions = []
    }

    parseResponse(command){
        return command.data.action_properties
    } 

    async listStories(){
        stories = await this.client.listStories().then(this.parseResponse).then(({stories}) => stories)
        return stories
    }

    async startStory(name){
        this.storyId = await this.client.startStory(name, this.lang).then(this.parseResponse).then(({story_id}) => story_id)
    }

    async getNewPromptsAndActions(){
        let {story_finished, prompts, moods, possible_user_actions} = await this.client.getStoryUntilNow(this.storyId).then(this.parseResponse).then((response) => response)
        this.storyFinished = story_finished
        let newPrompts = prompts.slice(this.promptIndex)
        let newMoods = moods.slice(this.promptIndex)
        this.promptIndex = prompts.length
        this.nextActions = possible_user_actions

        return {newPrompts, newMoods, nextActions: this.nextActions}
    }

    async executeAction(index){
        await this.client.executeAction(this.storyId, index)
    }

}

/**
 * The loop should be
 * manager = new StoryTellingManager()
 * ...
 * while(!manager.storyFinished){
 *     {newPrompts, newMoods, nextActions} ) manager.getNewPromptsAndActions()
 *     ...
 *     manager.executeAction(index)
 * }
 */ 
