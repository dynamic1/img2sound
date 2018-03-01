<template>
  <div id="app">
    <div class="container">
        <img :src="imageSrc" v-if="imageSrc" class="image" style="width:600px;height=400px">
        <input @change="uploadImage" type="file" name="sound_file" accept="sound/*">
        <audio controls v-if="audioSrc">
          <source :src="audioSrc" type="audio/wav">
        </audio>
        xalex
    </div>  
    <div>
      <p>
      file_id: {{ sound_file_id}}
      </p>
      imgSrc: {{ imageSrc }}
      <p>
      audioSrc: {{ audioSrc }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "app",
  data() {
    return {
      imageSrc: "",
      audioSrc: "",
      sound_file_id: ""

    };
  },

  methods: {
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
        .post("//localhost:5000/api/v1/spectrogram", data, {
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
          this.imageSrc = "http://localhost:5000/api/v1/spectrogram?file_id=" + this.sound_file_id
          this.audioSrc = "http://localhost:5000/uploads/" + this.sound_file_id + ".wav"
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
