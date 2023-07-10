import subprocess

# C#のコードをコンパイル
subprocess.run(['dotnet','Mizuyari_app.csproj'])

# 実行可能なファイル（DLLやEXE）を指定して実行
result = subprocess.run(['dotnet', 'Mizuyari_app/bin/Debug/net6.0-windows/Mizuyari_app.dll'], capture_output=True, text=True)
output = result.stdout
print(output)
