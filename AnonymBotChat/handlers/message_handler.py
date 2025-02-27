from database import ProfileDB

db = ProfileDB
class MessageHandler:
    def __init__(self, bot, user_manager):
        self.bot = bot
        self.user_manager = user_manager

        # Регистрируем обработчики сообщений (кроме команд)
        self.bot.message_handler(
            func=lambda message: not self.is_command(message),
            content_types=['text', 'photo', 'document', 'audio', 'video', 'voice', 'sticker', 'location', 'contact']
        )(self.handle_message)

    def is_command(self, message):
        """Проверяет, является ли сообщение командой."""
        return message.content_type == 'text' and message.text.startswith('/')

    def handle_message(self, message):
        user_id = message.from_user.id
        partner_id = self.user_manager.get_partner(user_id)

        if not partner_id:
            self.bot.send_message(user_id, 'Вы не в чате. Нажмите /search чтобы найти собеседника.')
            return

        try:
            # Пересылка текстовых сообщений
            if message.text:
                self.bot.send_message(partner_id, message.text)

            # Пересылка фото
            elif message.photo:
                self.bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)

            # Пересылка аудио
            elif message.audio:
                self.bot.send_audio(partner_id, message.audio.file_id, caption=message.caption)

            # Пересылка видео
            elif message.video:
                self.bot.send_video(partner_id, message.video.file_id, caption=message.caption)

            # Пересылка документов
            elif message.document:
                self.bot.send_document(partner_id, message.document.file_id, caption=message.caption)

            # Пересылка голосовых сообщений
            elif message.voice:
                self.bot.send_voice(partner_id, message.voice.file_id)

            # Пересылка стикеров
            elif message.sticker:
                self.bot.send_sticker(partner_id, message.sticker.file_id)

            # Пересылка местоположения
            elif message.location:
                self.bot.send_location(partner_id, message.location.latitude, message.location.longitude)

            # Пересылка контактов
            elif message.contact:
                self.bot.send_contact(
                    partner_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name
                )

            # Пересылка других типов сообщений (например, анимации, опросов и т.д.)
            else:
                self.bot.forward_message(partner_id, message.chat.id, message.message_id)

        except Exception as e:
            print(f"Ошибка при пересылке сообщения: {e}")
            self.bot.send_message(user_id, 'Произошла ошибка при пересылке сообщения.')