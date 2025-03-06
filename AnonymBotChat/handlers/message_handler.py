from telebot import types
from utils.user_manager import UserManager  # Импортируем UserManager

class MessageHandler:
    def __init__(self, bot, user_manager: UserManager):  # Указываем тип user_manager
        self.bot = bot
        self.user_manager = user_manager

        # Регистрируем обработчики сообщений (кроме команд)
        self.bot.message_handler(
            func=lambda message: not self.is_command(message),
            content_types=['text', 'photo', 'document', 'audio', 'video', 'voice', 'sticker', 'location', 'contact', 'video_note']
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
            # Если это ответ на сообщение (реплай)
            if message.reply_to_message:
                # Пересылаем сообщение с реплаем
                self.forward_with_reply(message, partner_id)
            else:
                # Пересылаем обычное сообщение
                self.forward_message(message, partner_id)

        except Exception as e:
            print(f"Ошибка при пересылке сообщения: {e}")
            self.bot.send_message(user_id, 'Произошла ошибка при пересылке сообщения.')

    def forward_message(self, message, partner_id):
        """Пересылает сообщение партнеру и возвращает отправленное сообщение."""
        if message.text:
            sent_message = self.bot.send_message(partner_id, message.text)
        elif message.photo:
            sent_message = self.bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)
        elif message.audio:
            sent_message = self.bot.send_audio(partner_id, message.audio.file_id, caption=message.caption)
        elif message.video:
            sent_message = self.bot.send_video(partner_id, message.video.file_id, caption=message.caption)
        elif message.document:
            sent_message = self.bot.send_document(partner_id, message.document.file_id, caption=message.caption)
        elif message.voice:
            sent_message = self.bot.send_voice(partner_id, message.voice.file_id)
        elif message.sticker:
            sent_message = self.bot.send_sticker(partner_id, message.sticker.file_id)
        elif message.location:
            sent_message = self.bot.send_location(partner_id, message.location.latitude, message.location.longitude)
        elif message.contact:
            sent_message = self.bot.send_contact(
                partner_id,
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name
            )
        elif message.video_note:
            sent_message = self.bot.send_video_note(partner_id, message.video_note.file_id)
        else:
            sent_message = self.bot.forward_message(partner_id, message.chat.id, message.message_id)

        # Сохраняем текст сообщения для корректного реплая
        if sent_message and message.text:
            self.user_manager.save_message_text(partner_id, message.message_id, message.text)

        return sent_message

    def forward_with_reply(self, message, partner_id):
        """Пересылает сообщение с реплаем, имитируя реплай."""
        # Получаем текст сообщения, на которое нужно ответить
        original_text = self.user_manager.get_message_text(partner_id, message.reply_to_message.message_id)

        if original_text:
            # Формируем текст с реплаем
            reply_text = f"Ответ на:\n{original_text}\n\n{message.text}"
            self.bot.send_message(partner_id, reply_text)
        else:
            # Если не удалось найти текст для реплая, отправляем обычное сообщение
            self.forward_message(message, partner_id)