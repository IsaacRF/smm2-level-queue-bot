#############################
#  SMM2 Level Queue Bot  #
#############################
Authors:         IsaacRF239 & Gabriel Rodríguez
License:         GNU General Public License v3.0
Project URL:     https://github.com/IsaacRF/smm2-level-queue-bot
Twitch Channel:  https://twitch.tv/hirokurai
Isaac Website:   https://isaacrf.com
Gabriel Website: https://www.gabrielrf.dev/

[English]
SMM2 Level Queue Bot is a Streamlabs bot / script that allows viewers to queue Super Mario Maker 2 levels, while offering all sort of commands to allow mods to refresh overlay or jump to next level in queue; and viewers to see their turn in queue, list levels, etc. SMM2LQS includes an animated overlay compatible with all main stream software such as OBS, Streamlabs OBS and XSplit to visualize the current and next level in queue.

[Español]
SMM2 Level Queue Bot es un bot / script de Streamlabs que permite a los usuarios añadir sus niveles a una cola, mientras que ofrece todo tipo de comandos para permitir que los moderadores hagan un refresh del overlay o salten al siguiente nivel de la cola; y a los viewers ver su turno en la cola, listar niveles, etc. SMM2LQS incluye un overlay animado compatible con cualquier software de stream, como OBS, Streamlabs OBS y XSplit, para visualizar en pantalla el nivel actual y el siguiente.

###################################
#     License and conditions      #
###################################
[English]
This project uses a GNU General Public License v3.0. This means that:
1.- You can freely use, copy, modify and redistribute this software, as long as it remains open source.
2.- You must keep original copyright information and notices. Removing them is not permitted.
3.- If you modify and / o redistribute this code, you must use the same license (GNU General Public License v3.0).

For more information on licensing and usage conditions, check the LICENSE file.

[Español]
Este proyecto utiliza una licencia GNU General Public License v3.0. Esto significa que:
1.- Puedes utilizar, copiar, modificar y redistribuir libremente este software, siempre y cuando lo mantengas de código abierto.
2.- Debes mantener la información y avisos de copyright originales. Eliminarlos no está permitido.
3.- Si modificas y/o redistribuyes este código, debes utilizar la misma licencia (GNU General Public License v3.0).

Para más información sobre la licencia y las condiciones de uso, echa un vistazo al archivo LICENSE.

#####################
#    Installation   #
#####################
[English]
1.- Import the bot into your Streamlabs Chatbot or Streamlabs OBS chatbot, into the "</> Scripts" section on left bar. If this section is not visible, remember to log into your Streamer and Bot accounts. You can import SMM2LQS by either of these two methods:
    A.- Press the import ->] button on the and select the bot .zip file, that's all.
    B.- Manually copy the bot folder into your scripts folder. You can find it by Right Clicking the back of the script lists in "</> Scripts" and selecting "Open Script Folder".

    This folder is usually located on "C:\Users\Username\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts"
2.- Right click the script and press "Insert API Key"
3.- On the right panel, configure your commands, limits, cooldowns and bot responses as you wish. You can instantly restore or translate default responses to English and Spanish using the buttons in the "Responses" section of the configuration
4.- If you want to use the integrated overlay, add a Browser view to your Stream soft, local file, and select the file /overlay/index.html. Recommended browser source size is 1400x250px, tweak these values until you get the desired size, and avoid resizing the graphic element in scene to avoid text blurriness.
NOTE: Overlay is firstly loaded empty, even if there are levels on queue. It will automatically update when win, skip or delete level commands are used, but you can force the refresh manually using the !refreshlevels command
5.- The bot is ready to go

[Español]
1.- Importa el bot en Streamlabs Chatbot o Streamlabs OBS chatbot, en el apartado "</> Scripts" de la barra lateral izquierda. Si no ves esta sección, recuerda hacer login en tus cuentas de Streamer y Bot. Puedes importar SMM2LQS de cualquiera de estas dos maneras:
    A.- Pulsa el botón "import" ->] en la parte superior derecha, y selecciona el .zip del bot, eso es todo.
    B.- Copia manualmente la carpeta del bot en tu carpeta de scripts. Puedes encontrarla haciendo click derecho en el fondo de la lista de scripts en "</> Scripts", y seleccionando "Open Script Folder".

    Este directorio suele estar localizado en "C:\Users\Username\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts"
2.- Haz click derecho en el script y selecciona "Insert API Key"
3.- En el panel de la derecha, configura tus comandos, límites, cooldowns y las respuestas del bot como prefieras. Puedes restaurar y traducir las respuestas por defecto a Inglés y Español usando los botones dentro de la sección "Responses" de la configuración
4.- Si quieres usar el overlay integrado, añade una Browser view en tu programa de stream, selecciona archivo local / local file, y selecciona el archivo /overlay/index.html que se encuentra dentro del bot. El tamaño del browser source recomendado es 1400x250px, modifica estos valores para adaptar el tamaño en lugar de redimensionar el elemento en la escena, ya que podría causar blur en los textos.

NOTA: Ten en cuenta que el overlay se carga vacío inicialmente aunque haya niveles en cola. Se actualizará automáticamente al utilizar los comandos de win, skip o delete level, pero también puedes forzar el refresh del overlay con el comando !refreshlevels
5.- El bot está listo para usar

#####################
#      Usage        #
#####################
NOTE: In this section, commands are referenced by their default name. You can change them in the configuration
NOTE 2: Advanced permission commands can only be executed by Caster or Mods by default. This can be changed in the "Permissions" section of the configuration.

--VIEWERS COMMANDS--
!smm2lqs : Info about commands that can be used

!add <code> : Adds a level code to queue. Code must be in XXX-YYY-ZZZ or XXX YYY ZZZ format, and must contain only alphanumeric characters, excluding punctuaction symbols and letters I, O. Bot will reject the level if it doesn't complain with the official SMM2 level code format. User that sent the level is also stored along the level code as in "XXX-YYY-ZZZ [@User]"

!list : Pretty prints a list of all the levels in queue

!position : Prints all the positions the viewer that used the command has levels into

!level : Info about the current level (First in queue)

!nextlevel : Info about the next level (Second in queue)

--ADVANCED PERMISSION COMMANDS--
!queueopen : Opens the queue

!queueclose : Closes the queue. This disables only !add command, all the other commands can still be executed

!winlevel : Jump to the next level in queue. Adds a Win to the wins counter

!skiplevel : Jump to the next level in queue. Adds a Skip to the skips counter

!deletelevel : Jump to the next level in queue, but lets the counters unaltered

!refreshlevels : Forces the overlay to refresh its data

#####################
#     Changelog     #
#####################
1.1.0 - Adds a levels overlay and adds responses to configuration
1.0.0 - Initial Release