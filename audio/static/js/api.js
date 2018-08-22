var api = {
  get_ayah: function(callback) {
    $.get("/get_ayah", function(data) {
      callback.call(this, data);
    })
  },
  get_specific_ayah: function(surah, ayah, callback) {
    $.ajax(
      {
        type: "POST",
        url: "/get_ayah/",
        data: { surah, ayah },
        dataType: "json",
        success: function (data) {
          try {
            localStorage.setItem("lastAyah", JSON.stringify(data))
            callback.call(this, data);
          } catch (e) {
            console.log(e.message)
          }
        }
      }
    );
    return false;
  },

  send_recording: function(audio, surah_num, ayah_num, hash_string) {
    var fd = new FormData();
    fd.append('file', audio, surah_num+"_"+ayah_num+"_"+hash_string+".wav");
    fd.append('surah_num', surah_num);
    fd.append('ayah_num', ayah_num);
    fd.append('hash_string', hash_string);
    $.ajax(
      {
        type: "POST",
        url: "/api/recordings/",
        data: fd,
        processData: false,
        contentType: false,
        complete: function(jqXHR, textStatus) {
          console.log(textStatus);
        }
      }
    )
  },

}
