<template>
  <div>
    <div v-for="profile in profile_list" v-bind:key="profile">
      <h1>{{profile.user.username}}</h1>
      <img :src="profile.image_url" width="100" height="100">
      <p>{{profile.bio}}</p>
    </div>
  </div>
</template>


<script>
import axios from "axios";
export default {
  name:"Index",
  data() {
    return {
      profile_list:[]
    }
  },
  created() {
    this.getAllProfiles()
  },
  methods: {
    getAllProfiles: function(){
      axios.get("http://127.0.0.1:8000/api/profile/").then(response=>{
        this.profile_list = response.data
      })
    }
  }
}
</script>
