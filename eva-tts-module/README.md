# Text-To-Speech Module #

This module is responsible for transforming texts (strings) into speech (audio files). To do this, it uses the *IBM-Watson* TTS cloud service. This module generates audio from text and stores it locally in cache, in the **TTS Cache Files** folder. Soon after, it uses the robot's Audio module to play the speech audio You can see how this works through Figure 1.

![alt text](eva-tts-view.png)
<p aligh="center">
<strong>Figure 1.</strong> The integration of the TTS and Audio modules in the generation and playback of the robot's speech audio.
</p>
</br>

**If the robot speaks phrases that have already been transformed into audio in a previous interaction, the TTS module searches for these phrases in the local cache, without having to use the cloud again. As a result, these phrases are spoken instantly by the robot.**


**For the robot to speak the text transformed into speech, it is necessary to have both modules running, the TTS module and the Audio module.**

## Module Dependencies

* **Paho-Mqtt 1.6.1** (It can be installed using pip)
* ***IBM-Watson*** (It can be installed using pip)

