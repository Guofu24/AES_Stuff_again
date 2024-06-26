from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from Crypto.Cipher import AES
from .models import Stuff
from .forms import StuffForm
import base64, os
from Crypto.Random import get_random_bytes
from django.conf import settings

# Function to generate a 16-byte AES key
def generate_key():
    return get_random_bytes(16)

#Hàm mã hóa dữ liệu hồ sơ
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    data = data + (AES.block_size - len(data) % AES.block_size) * b"\0"
    encrypted_data = cipher.encrypt(data)
    return base64.b64encode(encrypted_data).decode('utf-8')

#Hàm giải hóa dữ liệu hồ sơ
def decrypt_data(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_data = decrypted_data.rstrip(b"\0")
    return decrypted_data.decode('utf-8')

#Hàm nhập khóa mã hóa hồ sơ
def get_key(request):
    if request.method == "POST":
        key = request.POST.get('encryption_key')
        if not key or len(key) != 16:
            return HttpResponseBadRequest("Khóa phải có độ dài 16 kí tự.")
        return key.encode()
    return HttpResponseBadRequest("Invalid request method")

#Hiển thị tạo nhân viên
def create_stuff(request):
    if request.method == 'POST':
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            #Xóa dữ liệu từ form
            Firstname = form.cleaned_data['Firstname']
            Lastname = form.cleaned_data['Lastname']
            Position = form.cleaned_data['Position']
            Year = form.cleaned_data['Year']
            Phone = form.cleaned_data['Phone']
            Address = form.cleaned_data['Address']
            
            #Khóa
            key = get_key(request)
            if isinstance(key, HttpResponseBadRequest):
                return key  
            
            try:
                #Mã hóa dữ liệu trước khi vào data
                encrypted_Firstname = encrypt_data(Firstname.encode('utf-8'), key)
                encrypted_Lastname = encrypt_data(Lastname.encode('utf-8'), key)
                encrypted_Position = encrypt_data(Position.encode('utf-8'), key)
                encrypted_Year = encrypt_data(Year.encode('utf-8'), key)
                encrypted_Phone = encrypt_data(Phone.encode('utf-8'), key)
                encrypted_Address = encrypt_data(Address.encode('utf-8'), key)
                
                #Lưu vào data
                stuff = form.save(commit=False)
                stuff.Firstname = encrypted_Firstname
                stuff.Lastname = encrypted_Lastname
                stuff.Position = encrypted_Position
                stuff.Year = encrypted_Year
                stuff.Phone = encrypted_Phone
                stuff.Address = encrypted_Address
                stuff.save()
                
                return redirect('success')
            
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
    else:
        form = StuffForm()
    return render(request, 'create_stuff.html', {'form': form})

#Code hiển thị thông tin giải mã
def stuff_list(request):
    if request.method == 'POST':
        key = get_key(request)
        if isinstance(key, HttpResponseBadRequest):
            return key  
        
        stuff = Stuff.objects.all()
        decrypted_stuff = []
        
        for item in stuff:
            try:
                decrypted_item = {
                    'id': item.id,
                    'Firstname': decrypt_data(item.Firstname, key),
                    'Lastname': decrypt_data(item.Lastname, key),
                    'Position': decrypt_data(item.Position, key),
                    'Year': decrypt_data(item.Year, key),
                    'Phone': decrypt_data(item.Phone, key),
                    'Address': decrypt_data(item.Address, key),
                }
                decrypted_stuff.append(decrypted_item)
            except ValueError:
                pass
        
        return render(request, 'stuff_list.html', {'decrypted_stuff': decrypted_stuff, 'key_required': False})
    
    else:
        stuff = Stuff.objects.all()
        return render(request, 'stuff_list.html', {'stuff': stuff, 'key_required': True})

#Xóa hồ sơ
def delete_stuff(request, stuff_id):
    stuff = get_object_or_404(Stuff, pk=stuff_id)
    
    if request.method == 'POST':
        key = get_key(request)
        if isinstance(key, HttpResponseBadRequest):
            return key
        
        try:
            
#            decrypt_data(stuff.Firstname, key)
            stuff.delete()
            return redirect('stuff_list')
        except ValueError:
            return HttpResponseBadRequest("Invalid encryption key.")
    
    return HttpResponseBadRequest("Invalid request method")

def delete_stuff1(request, stuff_id):
    stuff = get_object_or_404(Stuff, pk=stuff_id)
    stuff.delete()
    return redirect('stuff_list')

#Sửa hồ sơ
def edit_stuff(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)   
    if request.method == 'POST':
        key = get_key(request)
        if isinstance(key, HttpResponseBadRequest):
            return key        
        try:
            decrypted_stuff = {
                'Firstname': decrypt_data(stuff.Firstname, key),
                'Lastname': decrypt_data(stuff.Lastname, key),
                'Position': decrypt_data(stuff.Position, key),
                'Year': decrypt_data(stuff.Year, key),
                'Phone': decrypt_data(stuff.Phone, key),
                'Address': decrypt_data(stuff.Address, key),
            }          
            #Cập nhật thông tin
            form = StuffForm(request.POST, instance=stuff, initial=decrypted_stuff)         
            if form.is_valid():
                #Xóa thông tin
                Firstname = form.cleaned_data['Firstname']
                Lastname = form.cleaned_data['Lastname']
                Position = form.cleaned_data['Position']
                Year = form.cleaned_data['Year']
                Phone = form.cleaned_data['Phone']
                Address = form.cleaned_data['Address']              
                try:
                    #Cập nhật mã hóa
                    encrypted_Firstname = encrypt_data(Firstname.encode('utf-8'), key)
                    encrypted_Lastname = encrypt_data(Lastname.encode('utf-8'), key)
                    encrypted_Position = encrypt_data(Position.encode('utf-8'), key)
                    encrypted_Year = encrypt_data(Year.encode('utf-8'), key)
                    encrypted_Phone = encrypt_data(Phone.encode('utf-8'), key)
                    encrypted_Address = encrypt_data(Address.encode('utf-8'), key)                  
                    #Lưu vào database
                    stuff.Firstname = encrypted_Firstname
                    stuff.Lastname = encrypted_Lastname
                    stuff.Position = encrypted_Position
                    stuff.Year = encrypted_Year
                    stuff.Phone = encrypted_Phone
                    stuff.Address = encrypted_Address
                    stuff.save()
                    return redirect('stuff_list')             
                except ValueError:
                    return HttpResponseBadRequest("Error encrypting data")       
        except ValueError:
            return HttpResponseBadRequest("Error decrypting data")   
    else:
        return render(request, 'edit_stuff.html', {'stuff': stuff, 'form': StuffForm(), 'key_required': True})
    return HttpResponseBadRequest("Invalid request")

def success(request):
    return render(request, 'success.html')

#Trang chủ
def home(request):
    return render(request, 'master.html')

def get_key1(request):
    if request.method == "POST":
        key = request.POST.get('key')
        if len(key) != 16:
            return HttpResponseBadRequest("Khóa phải có độ dài 16 kí tự")
        return key.encode()  
    return None

# Hàm tải file lên
def handle_uploaded_file(uploaded_file):
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

# Hàm mã hóa file
def encrypt(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(nonce)
        file.write(tag)
        file.write(ciphertext)
    return encrypted_file_path

# Hàm giải mã file
def decrypt(file_path, key, new_filename):
    with open(file_path, 'rb') as file:
        nonce = file.read(16)
        tag = file.read(16)
        ciphertext = file.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    
    new_filename = os.path.basename(new_filename)  
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)
    
    with open(new_file_path, 'wb') as file:
        file.write(plaintext)
    return new_file_path

# Hàm tải mã hóa file
def encrypt_file(request):
    if request.method == 'POST' and 'encrypt' in request.POST:
        uploaded_file = request.FILES['file']
        file_path = handle_uploaded_file(uploaded_file)
        key = get_key1(request)
        if isinstance(key, HttpResponseBadRequest):
            return key
        encrypted_file_path = encrypt(file_path, key)
        
        # Tạo response để tải file
        with open(encrypted_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(encrypted_file_path)}'
            return response
    return render(request, 'encrypt.html')

# Hàm tải giải mã file
def decrypt_file(request):
    if request.method == 'POST' and 'decrypt' in request.POST:
        uploaded_file = request.FILES['file']
        file_path = handle_uploaded_file(uploaded_file)
        key = get_key1(request)
        if isinstance(key, HttpResponseBadRequest):
            return key
        new_filename = request.POST.get('new_filename')
        decrypted_file_path = decrypt(file_path, key, new_filename)
        
        # Tạo response để tải file
        with open(decrypted_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(decrypted_file_path)}'
            return response
    return render(request, 'decrypt.html')
