
with open("./sentences/cs_functions_sdk_api_sequences_with_only_api_call_8_11.txt","r") as f:
	data = f.readlines()

	for line in data:
		with open("./sentences/cs_functions_sdk_api_sequences_with_only_api_call.txt","a") as f1:
			f1.write(line)