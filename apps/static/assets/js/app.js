class Chatbox {
    constructor(options){
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            voiceButton: document.querySelector('.voice__button')
        }
        this.recordS = false;
        this.state = false;
        this.messages = [];
    }
    speechapi(){
        // var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
        // var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
    
        var grammar = '#JSGF V1.0;'
    
        var recognition = new SpeechRecognition();
        var speechRecognitionList = new SpeechGrammarList();
        speechRecognitionList.addFromString(grammar, 1);
        recognition.grammars = speechRecognitionList;
        recognition.lang = 'vi-VN';
        recognition.interimResults = false;
        recognition.onresult = function(event) {
            var lastResult = event.results.length - 1;
            var content = event.results[lastResult][0].transcript;
        };

        recognition.onspeechend = function() {
            recognition.stop();
        };

        recognition.onerror = function(event) {
            console.log('Error occurred in recognition: ' + event.error);
        }
        document.querySelector('.voice__button').addEventListener('click', function(){
            recognition.start();
        });
    }
    text2speak(text){
        var synthesis = window.speechSynthesis;
          
        // Get the first `en` language voice in the list
        var voice = synthesis.getVoices().filter(function (voice) {
          return voice.lang === 'vi';
        })[0];
      
        // Create an utterance object
        var utterance = new SpeechSynthesisUtterance(text);
      
        // Set utterance properties
        utterance.voice = voice;
        utterance.pitch = 1;
        utterance.rate = 1;
        utterance.volume = 0.8;
      
        // Speak the utterance
        synthesis.speak(utterance);
    }

    display() {
        const {openButton, chatBox, sendButton, voiceButton} = this.args;
        
        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        voiceButton.addEventListener('click', () => this.onVoiceButton(chatBox))

        var node = chatBox.querySelector('input');
        node.addEventListener("keypress", key_event);
        function key_event(e) {
            if (e.key === 'enter'){
                this.onSendButton(chatBox)
            }
        }
    }

    toggleState(chatbox){
        this.state = !this.state;
        // show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active')
            fetch("http://127.0.0.1:5000/welcome", {
                method: 'POST',
                body: JSON.stringify(),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(r => r.json())
            .then(r => {
                let msg = {name: "Sam", message: r};

                // this.text2speak(msg.message)
                console.log(msg.message)
                this.messages.push(msg);
                this.updateChatText(chatbox)
            }).catch((error) => {
                console.log('Error: ', error);
                this.updateChatText(chatbox)
            });
        }
        else{
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox){
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 == ""){
            return;
        }

        let msg1 = {name: "User", message: text1}
        this.messages.push(msg1);
        // 'http://127.0.0.1:5000/predict
        fetch("http://127.0.0.1:5000/predict", {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = {name: "Sam", message: r.answer};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''
        }).catch((error) => {
            console.error('Error: ', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    onVoiceButton(chatbox){
        var grammar = '#JSGF V1.0;'
        var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
        var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
        var recognition = new SpeechRecognition();
        var speechRecognitionList = new SpeechGrammarList();
        speechRecognitionList.addFromString(grammar, 1);
        recognition.grammars = speechRecognitionList;
        recognition.lang = 'vi-VN';
        recognition.interimResults = false;
        var content;
        if (!this.recordS){
            recognition.start();
            console.log("starting")
            recognition.onerror = function(event) {
                // message.textContent = 'Error occurred in recognition: ' + event.error;
                console.log(event.error)
            }

            recognition.onresult = function(event) {
                var lastResult = event.results.length - 1;
                content = event.results[lastResult][0].transcript;
                console.log(content)
                var chatmessage = chatbox.querySelector('.chatbox__messages');
                chatmessage.textField = content
                // content = content.json()
            }
            recognition.onspeechend = function() {
                recognition.stop();
                
            }
            this.recordS = true;
        }
        else {
            var chatmessage = chatbox.querySelector('.chatbox__messages');
            content = chatmessage.textField;
            console.log(content)
            let msg1 = {name: "User", message: content}
            this.messages.push(msg1);
            this.updateChatText(chatbox)
            // 'http://127.0.0.1:5000/voice_predict
            fetch("http://127.0.0.1:5000/voice_predict", {
                method: 'POST',
                body: JSON.stringify({message: content}),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(r => r.json())
            .then(r => {
                // let msg2 = {name: "User", message: r.question}
                // this.messages.push(msg2)
                let msg3 = {name: "Sam", message: r.answer};
                this.messages.push(msg3);
                this.updateChatText(chatbox)
            }).catch((error) => {
                // console.error('Error: ', error);
                this.updateChatText(chatbox)
            });
            this.recordS = false;
        }
        };

    updateChatText(chatbox){
        var html = '';
        this.messages.slice().reverse().forEach(function(item, number){
            if (item.name==="Sam"){

            html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
        }
        else
        {
            html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
        }
    });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display()