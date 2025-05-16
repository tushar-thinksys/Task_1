create a virtual env in python
run command:
pip install -r requirements.txt
in a second terminal run:
localstack start
in other terminal run:
uvicorn app.main:app --reload
type "image" or "audio" in file upload endpoint 

features not upto mark currently:
patch api's
currently only single api for both image and audio upload,
file format checks not implmented as causing issue[code commented out] 
presigned url not returned currently[code commented out]
