class SpeechRecognitionApi{
    constructor(options) {
        const SpeechToText = window.speechRecognition || window.webkitSpeechRecognition;
        this.speechApi = new SpeechToText();
        this.speechApi.lang = 'vi-VN'
        this.speechApi.continuous = true;
        this.speechApi.interimResults = false;
        this.output = options.output ? options.output : document.createElement('div');
        console.log(this.output)
        this.speechApi.onresult = (event)=> { 
            console.log(event);
            var resultIndex = event.resultIndex;
            var transcript = event.results[resultIndex][0].transcript;

            console.log('transcript>>', transcript);
            console.log(this.output)
            this.output.textContent = transcript;

            
        }
    }
    init(){
        this.speechApi.start();
    }
    stop(){
        this.speechApi.stop();
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
}
export class SpeechRecognitionApi{}