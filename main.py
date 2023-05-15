import asyncio
import aiogram
import intrepretator2
import code

#intrepretator2.start()

main_loop = asyncio.new_event_loop()
asyncio.set_event_loop(main_loop)
main_loop.run_until_complete(code.start())
aiogram.executor.start_polling(intrepretator2.bot_dispatcher_main)
main_loop.run_forever()


