from aiogram import F, Router
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .bot_states import Menu
from .kb import menu, resumes_kb, vacs_kb
from .reqs import get_user_access_token
from .errors import TokenError


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text='Добрый день')
    data: dict = await state.get_data()
    if not data.get('api_key'):
        await state.set_state(Menu.get_token)
        await message.answer(text='Перейдите по ссылке и пришлите нам токен', reply_markup=menu)
    else:
        await state.set_state(Menu.get_token)
        await message.answer(text='Перейдите по ссылке и пришлите нам токен', reply_markup=menu)


@router.message(Menu.get_token)
async def get_token(message: Message, state: FSMContext):
    
    token = message.text
    token_req = await get_user_access_token(token=token)
    
    access_token = token_req.get('access_token')
    refresh_token = token_req.get('refresh_token') 
    
    if token_req.get('status'):
        await state.set_data({
                'access_token': access_token,
                'refresh_token': refresh_token,
            })
        
        await message.answer(text='Успешно создали access_token')
        resumes_b = await resumes_kb(token=access_token)
        await message.answer(text='Выберите своё резюме', reply_markup=resumes_b)
    else:
        await message.answer(text='Похоже что вы ввели неправильный токен авторизации, попробуйте ещё раз\nПерейдите по ссылке и пришлите нам токен', reply_markup=menu)
        await state.set_state(Menu.get_token)


@router.callback_query(F.data=='resume_choice')
async def resumes_back(callback:CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    access_token = data.get('access_token')
    resumes_b = await resumes_kb(token=access_token)
    await callback.message.answer(text='Выберите своё резюме', reply_markup=resumes_b)
    await state.set_state(Menu.resume_choice)


@router.callback_query(F.data.regexp(r'resume:'))
async def resume_choice(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    resume_id = callback.data.split(":")[-1]
    data = await state.get_data()
    kb = await vacs_kb(access_token=data.get('access_token'), resume_id=resume_id)
    await callback.message.answer(text=f'Вот список вакансий', reply_markup=kb)


#Handle Error
@router.error(ExceptionTypeFilter(TokenError))
async def handle_error(exception: Exception, state: FSMContext):
    #Тут не очень хорошо всё сделано
    
    text_exception = str(exception.exception.args[0])
    event_type = 'message' if exception.update.message else 'callback_query'
    
    if 'токен' in text_exception:
        match event_type:
            case 'callback_query':
                await exception.update.callback_query.message.answer(text='Произошла ошибка с вашим токеном\nПерейдите по ссылке и пришлите нам новый токен', reply_markup=menu)
            case 'message':
                await exception.update.message.answer(text='Произошла ошибка с вашим токеном\nПерейдите по ссылке и пришлите нам новый токен', reply_markup=menu)
        await state.set_state(Menu.get_token)
        print('Произошла ошибка с токеном')
    else:
        print(f"Unexpected Error: {text_exception}")
    pass