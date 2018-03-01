import os
import json
import hashlib

import librosa.core as lc
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#mpl.use('TkAgg')

from flask import current_app as app
from flask import request, g, send_from_directory
from flask_restful import reqparse, abort, Resource
from flask_cors import cross_origin

from werkzeug import secure_filename


class CreateSpectrogram(Resource):
    
    # @cross_origin()
    def post(self):
        # for n,v in request.items():
            # print(f"{n}: {v}" )
        # return dir(request)
        print
        print(f"headers: {json.dumps(list(request.headers), indent=4)}")
        data = {
        }
        print(request.files)
        for k,l in request.files.items():
            # print(f"received uploaded file {uploaded_file.filename}")
            print(f"key of type {type(k)}, l of type {type(l)}")
            print(f"{k}: {l}")
            # print(f"uploaded file: {uploaded_file.items()}")
        # print(request.__dict__)
        uploaded_file = request.files['sound_file']
        print(f"uploaded file: {uploaded_file}")

        BLOCKSIZE = 65534

        hasher=hashlib.sha1()
        
        buf=uploaded_file.read(BLOCKSIZE)
        while len(buf)>0:
            hasher.update(buf)
            buf=uploaded_file.read(BLOCKSIZE)
            print("read")
        # reset the file stream because we have read it while hashing
        uploaded_file.stream.seek(0)
        file_hash = hasher.hexdigest()
        print(f"hash: {file_hash}")


        # file_hash = "asdfasdfasdf"     
        file_hash = secure_filename(file_hash)   
        new_file_name = file_hash + '.wav'
        # upload_folder=os.path.join(app.config.storage_path, app.config['UPLOADS']
        full_file_name = os.path.join( app.config.uploads_path, new_file_name)
        uploaded_file.save( full_file_name, BLOCKSIZE)
        uploaded_file.close()
        print(f"saved to {new_file_name}")
        data['file_id'] = file_hash
        

        # generate spectrogram .png file and store in storage/spectrograms folder
        # file_id = "sample2.wav"
        # file_id = new_file_name
        # source_file = 'uploads/' + file_id
        print(f"loading {full_file_name}")
        audio_data, sample_rate = lc.load(full_file_name, sr=None)

        spectrum, freq, tt, img = plt.specgram(x=audio_data, NFFT=512, Fs=sample_rate, noverlap=384, pad_to=None, sides='default')
        plt.axis('off')

        spectrogram_file_name = os.path.join(app.config.spectrograms_path, file_hash + '.png')
        print(f"sample_rate is {sample_rate}")

        plt.savefig(spectrogram_file_name, bbox_inches='tight', pad_inches=0, dpi=300, frameon=False)
        plt.close()
        
        data['sample_rate'] = sample_rate
        return data
        

    # @cross_origin()   
    
    def get(self):
        print(request)

        
        file_id = "sample2.wav"
        file_id = request.args['file_id']
        spectrogram_file_name = file_id + '.png'
        """
        source_file = 'uploads/' + file_id
        audio_data, sample_rate = lc.load(source_file)

        spectrum, freq, tt, img = plt.specgram(x=audio_data, NFFT=512, Fs=sample_rate, noverlap=384, pad_to=None, sides='default')
        plt.axis('off')

        print(f"sample_rate is {sample_rate}")

        plt.savefig('spectrograms/'+ spectrogram_file_name, bbox_inches='tight', pad_inches=0, dpi=300, frameon=False)
        """
        # return "asdf"
        print(f"sending {spectrogram_file_name} from {app.config.spectrograms_path}")
        return send_from_directory(app.config.spectrograms_path, spectrogram_file_name, mimetype='image/png')
    
    