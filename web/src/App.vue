<template>
  <div id="app">
    <div class="container">
        <label for="sound_file">Upload audio file so see</label>
        <input @change="uploadImage" type="file" name="sound_file" accept="audio/*">
    </div>
    <div class="container">
      <img :src="imageSrc" v-if="imageSrc" class="image" style="width:600px;height=400px">
    </div>
    <div class="container">
      <audio controls v-if="audioSrc">
        <source :src="audioSrc" type="audio/wav">
      </audio>
    </div>  
    <div class="container" v-if="debug">
      <p>
      file_id: {{ sound_file_id}}
      </p>
      imgSrc: {{ imageSrc }}
      <p>
      audioSrc: {{ audioSrc }}
      </p>
    </div>
    <div class="container">
      <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" v-on:vdropzone-success="afterUploadOk">
      </vue-dropzone>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.css'

export default {
  name: "app",
  components: {
    vueDropzone: vue2Dropzone
  },
  data() {
    return {
      imageSrc: "",
      audioSrc: "",
      sound_file_id: "",
      dropzoneOptions: {
          // url: '/api/v1/spectrogram',
          // url: 'http://localhost:5000/api/v1/spectrogram',
          url: '/api/v1/spectrogram',
          method: 'post',
          thumbnailWidth: 150,
          maxFilesize: 50,
          headers: { 
            // "Content-Type": "multipart/form-data",
            Accept: "application/json, text/plain, */*",
            'Access-Control-Allow-Origin': "*" 
          },
          paramName: 'sound_file'
      },
      debug: false

    };
  },


  methods: {

    afterUploadOk: function(file,response) {
        console.log("POST request completed:")
        console.log("got response: " + JSON.stringify(response));
        console.log("sound_file_id=" + response.file_id)
        
        this.sound_file_id = response.file_id;
        this.imageSrc = "/api/v1/spectrogram?file_id=" + this.sound_file_id
        this.audioSrc = "/uploads/" + this.sound_file_id + ".wav"
        console.log("imageSrc: " + this.imageSrc)
    },

    uploadImage: function(e) {
      var files = e.target.files;
      if (!files[0]) {
        return;
      }
      var data = new FormData();
      data.append("sound_file", files[0]);

      // var reader = new FileReader();
      // reader.onload = e => {
        // this.imageSrc = e.target.result;
      // };
      axios
        .post("/api/v1/spectrogram", data, {
          headers: {
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*"
          }
        })
        .then( response => {
          console.log("POST request completed:")
          console.log(response.data);
          console.log("sound_file_id=" + response.data.file_id)
          
          this.sound_file_id = response.data.file_id;
          this.imageSrc = "/api/v1/spectrogram?file_id=" + this.sound_file_id
          this.audioSrc = "/uploads/" + this.sound_file_id + ".wav"
          console.log("imageSrc: " + this.imageSrc)
          // reader.readAsDataURL(files[0]);
        })
        .catch(function(error) {
          console.log(error); // catch your error
        });
    }
  }
};
</script>
<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
