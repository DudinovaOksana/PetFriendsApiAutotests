from api import PetFriends
from settings import valid_email, invalid_email, valid_password

pf = PetFriends()


# тест на получение аутификационного ключа
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


#проверяем можно ли получить список всех животных  с корректными данными
def test_get_all_pets_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert len(result['pets']) > 0


# проверяем можно ли создать животное без фото с корректными данными
def test_create_pet_without_photo():
    age = "1"
    name = "Max"
    type = "python"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, type, age)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type


# проверяем можно ли добавить фото животного с корректными данными
def test_add_pet_photo():
    age = "4"
    name = "Ярослав"
    animal_type = "змея"
    pet_photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\pyt.jpg"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, animal_type, age)
    new_status, new_result = pf.set_pet_photo(auth_key, result["id"], pet_photo)
    assert new_status == 200


# проверяем можно ли создать фото животного с корректными данными
def test_create_pet_with_photo():
    age = "1"
    name = "Anton"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077.750.png"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, photo)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type
    assert "data:image/jpeg;base64" in result['pet_photo']


# проверяем можно ли обновить данные о животном с корректными данными
def test_sucsessful_update_pet_info():
    age = "5"
    name = "Змей-горыныч"
    animal_type = "гадюка"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.change_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')


# проверяем можно ли уорректно удалить животное
def test_sucessful_delete_pet():
    age = "1"
    name = "Yura_1"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077.750.png"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, photo)
    status_delete, result_delete = pf.delete_pet(auth_key, result["id"])
    assert status_delete == 200


# проверяем выдаст ли система ошибку при запросе ключей api с некорректным эл.ящиком
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# проверяем выдаст ли система ошибку при создании животного без фото без поля "animal_type"
def test_create_pet_without_photo_without_animal_type_field():
    age = '2'
    name = "Mark"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple_without_photo_without_animal_type_field(auth_key, name, age)
    assert status == 400


# проверяем выдаст ли система ошибку при создании животного без фото при отсутствии с некорректным auth-key
def test_create_pet_without_photo_with_invalid_auth_key():
    age = "2"
    name = "Mark"
    animal_type = "Медведь"
    status, result = pf.add_new_pet_simple_without_photo(auth_key={'key': 'incorrect_key'}, name=name, animal_type=animal_type, age=age)
    assert status == 403


# проверяем можно ли создать питомца с фото, где вместо фото загружен текстовый файл
def test_create_pet_with_invalid_photo():
    age = "3"
    name = "Michelle"
    type = "cat"
    pet_photo = "D:\\PycharmProjects\\PetFriendsApiAutotests\\images\\photo.txt"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, pet_photo)
    assert status == 400


# проверяем можно создать питомца с фото с некорректным auth_key
def test_create_pet_with_photo_with_invalid_auth_key():
    age = "2"
    name = "John"
    type = "cobra"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077.750.png"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key={'key': 'incorrect_key'}, name=name, animal_type=type, age=age, pet_photo=photo)
    assert status == 403


# проверяем можно ли добавить фото питомца с некорректным auth-key
def test_add_pet_photo_invalid_auth_key():
    age = "3"
    name = "Yan"
    type = "snake"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, type, age)
    pet_photo = "D:\\PycharmProjects\\PetFriendsApiAutotests\\images\\1575050853qqw.gif"
    status, result = pf.set_pet_photo(auth_key={'key': 'incorrect_key'}, pet_id=result["id"], pet_photo=pet_photo)
    assert status == 403


# проверяем можно ли получить список питомцев с некорректным ключом
def test_get_all_pets_with_invalid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key={'key': 'incorrect_key'}, filter="")
    assert status == 403


# проверяем можно ли удалить питомца с некорректным auth_key
def test_delete_pet_with_invalid_auth_key():
    age = "2"
    name = "Yura_2"
    type = "python"
    photo = "D:\PycharmProjects\PetFriendsApiAutotests\images\8077.750.png"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, photo)
    new_status, new_result = pf.delete_pet(auth_key={'key': 'incorrect_key'}, pet_id=result["id"])
    assert new_status == 403


# проверяем можно ли обновить сведения о питомце с некорректными данными
def test_update_pet_info_with_invalid_data():
    age = "5"
    name = "Kirill"
    animal_type = "Elefant"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.change_pet(auth_key, "ID_DOESN'T_EXIST", name, animal_type, age)
    assert status == 400


# проверим можно ли обновить данные о питомце с некорректным auth_key
def test_update_pet_info_with_invalid_auth_key():
    age = "5"
    name = "Kirill"
    animal_type = "Elefant"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.change_pet(auth_key={'key': '12345'}, pet_id=my_pets['pets'][0]['id'], name=name, animal_type=animal_type, age=age)
    assert status == 403
