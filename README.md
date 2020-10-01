# SMM2 Level Queue Bot
<p align="center">
  <img src="https://github.com/IsaacRF/smm2-level-queue-bot/blob/master/SMM2LQS_icon.png" width="50%" style="display: block; margin: 0 auto; text-align: center">
</p>

## Quick Links
- [👉 Setup](https://github.com/IsaacRF/smm2-level-queue-bot#setup)
- [👉 Commands](https://github.com/IsaacRF/smm2-level-queue-bot#commands)

## About
- Authors:         IsaacRF239 & Gabriel Rodríguez
- License:         GNU General Public License v3.0
- Twitch Channel:  https://twitch.tv/hirokurai
- Isaac Website:   https://isaacrf.com
- Gabriel Website: https://twitter.com/gabri239

### [English]
SMM2 Level Queue Bot is a Streamlabs bot / script that allows viewers to queue Super Mario Maker 2 levels, see their turn in the queue, list levels, etc., while offering all sorts of commands for mods to refresh the overlay or jump to the next level in the queue. SMM2LQS includes an animated overlay, compatible with all main streaming software such as OBS, Streamlabs OBS and XSplit to visualize the current and next level in queue.

### [Español]
SMM2 Level Queue Bot es un bot / script de Streamlabs que permite a los viewers añadir sus niveles a una cola, ver su turno en la cola, listar niveles, etc., mientras que ofrece todo tipo de comandos para permitir que los moderadores hagan un refresh del overlay o salten al siguiente nivel de la cola. SMM2LQS incluye un overlay animado compatible con cualquier software de stream, como OBS, Streamlabs OBS y XSplit, para visualizar en pantalla el nivel actual y el siguiente.

![SMM2 Level Queue Bot Demo](https://user-images.githubusercontent.com/2803925/94565241-3e00e600-0269-11eb-8295-e89eb9ff51ae.gif)

## License and conditions
### [English]
This project uses a GNU General Public License v3.0. This means that:
1. You can freely use, copy, modify and redistribute this software, as long as it remains open source.
2. You must keep original copyright information and notices. Removing them is not permitted.
3. If you modify and/or redistribute this code, you must use the same license (GNU General Public License v3.0).

For more information on licensing and usage conditions, check the [LICENSE](https://github.com/IsaacRF/smm2-level-queue-bot/blob/master/LICENSE) file.

### [Español]
Este proyecto utiliza una licencia GNU General Public License v3.0. Esto significa que:
1. Puedes utilizar, copiar, modificar y redistribuir libremente este software, siempre y cuando lo mantengas de código abierto.
2. Debes mantener la información y avisos de copyright originales. Eliminarlos no está permitido.
3. Si modificas y/o redistribuyes este código, debes utilizar la misma licencia (GNU General Public License v3.0).

Para más información sobre la licencia y las condiciones de uso, echa un vistazo al archivo [LICENSE](https://github.com/IsaacRF/smm2-level-queue-bot/blob/master/LICENSE).

## Setup
### [English]
1. Download the bot [here](https://github.com/IsaacRF/smm2-level-queue-bot/releases)
2. Import the bot into your Streamlabs Chatbot or Streamlabs OBS chatbot, into the "</> Scripts" section on left bar. ***If this section is not visible, remember to log in to your Streamer and Bot accounts***. You can import SMM2LQS by either of these two methods:
    1. Press the import ->] button on the upper right section and select the bot's .zip file, that's all.
    2. Manually copy the bot folder into your scripts folder. You can find it by Right Clicking the background of the scripts list in "</> Scripts" and selecting "Open Script Folder".

    This folder is usually located on "C:\Users\Username\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts"
3. Right click the script and press "Insert API Key"
4. On the right panel, configure your commands, limits, cooldowns and bot responses as you wish. You can instantly restore or translate default responses to English and Spanish using the buttons in the "Responses" section of the configuration
5. If you want to use the integrated overlay, add a Browser view to your streaming software, select local file, and then select the file /overlay/index.html. Recommended browser source size is 1400x250px, tweak these values until you get the desired size, and avoid resizing the graphic element in scene to avoid text blurriness.
***NOTE**: The overlay is loaded empty at first, even if there are levels in the queue. It will automatically update when the win, skip or delete level commands are used, but you can force the refresh manually by running the !refreshlevels command*
6. The bot is ready to go.

### [Español]
1. Descarga el bot desde [aquí](https://github.com/IsaacRF/smm2-level-queue-bot/releases)
2. Importa el bot en Streamlabs Chatbot o Streamlabs OBS chatbot, en el apartado "</> Scripts" de la barra lateral izquierda. ***Si no ves esta sección, recuerda hacer login en tus cuentas de Streamer y Bot***. Puedes importar SMM2LQS de cualquiera de estas dos maneras:
    1. Pulsa el botón "import" ->] en la parte superior derecha, y selecciona el .zip del bot, eso es todo.
    2. Copia manualmente la carpeta del bot en tu carpeta de scripts. Puedes encontrarla haciendo click derecho en el fondo de la lista de scripts en "</> Scripts", y seleccionando "Open Script Folder".

    Este directorio suele estar localizado en "C:\Users\Username\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts"
3. Haz click derecho en el script y selecciona "Insert API Key"
4. En el panel de la derecha, configura tus comandos, límites, cooldowns y las respuestas del bot como prefieras. Puedes restaurar y traducir las respuestas por defecto a Inglés y Español usando los botones dentro de la sección "Responses" de la configuración
5. Si quieres usar el overlay integrado, añade una Browser view en tu programa de stream, selecciona archivo local / local file, y selecciona el archivo /overlay/index.html que se encuentra dentro del bot. El tamaño del browser source recomendado es 1400x250px, modifica estos valores para adaptar el tamaño en lugar de redimensionar el elemento en la escena, ya que podría causar blur en los textos.
***NOTA**: Ten en cuenta que el overlay se carga vacío inicialmente aunque haya niveles en cola. Se actualizará automáticamente al utilizar los comandos de win, skip o delete level, pero también puedes forzar el refresh del overlay con el comando !refreshlevels*
6.- El bot está listo para usar

## Commands
***NOTE**: In this section, commands are referenced by their default name. You can change them in the configuration*

***NOTE 2**: Advanced permission commands can only be executed by Caster or Mods by default. This can be changed in the "Permissions" section of the configuration.*

### Viewers Commands
- **!smm2lqs** : Info about commands that can be used
- **!add [code]** : Adds a level code to the queue. Code must be in XXX-YYY-ZZZ or XXX YYY ZZZ format, and must contain only alphanumeric characters, excluding punctuaction symbols and the letters I and O. The bot will reject the level if it doesn't comply with the official SMM2 level code format. The user that sent the level is also stored along with the level code, as in "XXX-YYY-ZZZ [@User]"
- **!list** : Pretty prints a list of all the levels in queue
- **!position** : Prints the positions, in the queue, of all the levels the viewer has added (if any)
- **!level** : Info about the current level (First in queue)
- **!nextlevel** : Info about the next level (Second in queue)

### Advanced Permission Commands
- **!queueopen** : Opens the queue
- **!queueclose** : Closes the queue. This disables only the !add command, all the other commands will still be available
- **!winlevel** : Jumps to the next level in the queue. Adds a Win to the wins counter
- **!skiplevel** : Jumps to the next level in the queue. Adds a Skip to the skips counter
- **!deletelevel** : Jumps to the next level in the queue, but leaving both counters unchanged
- **!refreshlevels** : Forces the overlay to refresh its data

## Technologies
- Python
- HTML5
- CSS
- SASS
- Javascript

## Changelog
### 1.1.0
- Adds a levels overlay and adds responses to configuration

### 1.0.0
- Initial Release
