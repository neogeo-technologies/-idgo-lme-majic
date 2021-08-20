
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  
  function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000)); // En jours
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/; Secure";
  }
  
  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
  function checkCookie(cname) {
    var extraction_ok = getCookie(cname);
    if (extraction_ok != "") {
      return extraction_ok;
    }
    else { return false}
  }
  
  
  function check_extract(statut="", url=""){
    var organisation = document.getElementById('0-organisation-input');
    var secret = document.getElementById('secret');
    var request_id = document.getElementById('request_id');
    var mode = document.getElementById('mode');
    let type = 'lme';

    if (mode.value)
        type = 'majic';
    params= {
      'organisation': organisation.value,
      'secret': secret.value,
      'request_id': request_id.value,
      'mode': mode.value,
      'statut': statut,
      'url': url,
    }
    axios({
      method: 'get',
      url: 'majic_check',
      params: params,
      headers: {'Content-Type': 'multipart/form-data' }
      })
      .then(function (response) {
          let response_html = '';
          // IF RESPONSE STATUT OK
          if (response.data.statut == 'OK'){
            console.log(type)
            setCookie('extraction-'+ type, secret.value + response.data.url, 1);
            response_html = response_ok(response.data.url, secret.value, request_id.value)
            }
          // IF RESPONSE STATUT PENDING
          if (response.data.statut == 'pending'){
            response_html = `<h5> Statut de la demande : En cours</h5>
                            <div class="loader"></div>`
            setTimeout(function(){ check_extract('pending', response.data.url); }, 30000);
          }
          // IF RESPONSE STATUT ERROR
          if (response.data.statut == 'error'){
            response_html = `<h5> Un erreur s'est produit lors de votre demande. Merci Contactez aux administrateurs du site.</h5>
                            <div class="spinner-border" role="status">
                            <div class="loader"></div>`
            setTimeout(function(){ check_extract()}, 3000);
          }
          set_response(response_html)
         
      })
      .catch(function (response) {
          //handle error
          console.log('erreur', response);
          msg_error = `<li>Une erreur s'est produit lors de la recuperation du fichier d'extraction. Contactez aux administrateur
                       du site.</li>`;
          show_msg_error(msg_error)
      });
  }
  function downloadFile(){
    var mode = document.getElementById('mode');
    let type = 'lme';
    if (mode.value)
        type = 'majic';
    var request_id = document.getElementById('request_id');
    params= {
      'request_id': request_id.value,
      'type': type,
    }
    axios({
        method: 'get',
        url: 'download_majic',
        params: params,
        // headers: {'Content-Type': 'multipart/form-data' },
        responseType: "blob",
        })
        .then(function (response) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'download_majic.7z');
          document.body.appendChild(link);
          link.click();
        })
        .catch(function (response) {
            //handle error
            console.log('erreur', response);
        });
  }


  function response_ok(url, secret, request_id){
    return `<h5> Télécharger l'extraction : 
            <a href="#" onclick="downloadFile();">
              Fichier zip
            </a>
          </h5>
          Code secret: ${secret}`
  }
  
  function set_response(response_html){
    $('#statut-id-0').html(`
      ${response_html}
    `);
    hiddenElement("download-form")
  }
  
  $("input:checkbox").on('click', function() {
    // in the handler, 'this' refers to the box clicked on
    var $box = $(this);
    if ($box.is(":checked")) {
      // the name of the box is retrieved using the .attr() method
      // as it is assumed and expected to be immutable
      var group = "input:checkbox[name='" + $box.attr("name") + "']";
      // the checked state of the group/box on the other hand will change
      // and the current value is retrieved using .prop() method
      $(group).prop("checked", false);
      $box.prop("checked", true);
    } else {
      $box.prop("checked", false);
    }
  });

  
  
  function init_majicLmeForm(){
    var organisationInput =  document.getElementById('0-organisation-input');
    if (organisationInput==null){
      hiddenElement('organisation-inputs');
    }
    $('#0-organisation-input').prop('checked', true);
    var fileDeclaration = document.getElementById('fileDeclaration');
    var listFileDeclaration = document.getElementById('list_file_declaration');
    var fileClause = document.getElementById('fileClause');
    var listFileClause = document.getElementById('list_file_clause');
    
    if (fileDeclaration !== null && fileDeclaration.value == '') {
      fileDeclaration.onchange = function () {
        var files = Array.from(this.files);
        files = files.map(file => file.name);
        listFileDeclaration.innerHTML = files.join('<br/>');
      }
    }
    if (fileClause !== null && fileClause.value == '') {
      fileClause.onchange = function () {
        var files = Array.from(this.files);
        files = files.map(file => file.name);
        listFileClause.innerHTML = files.join('<br/>');
      }
    }
  }
  
  $(document).ready(function() {
    // majic-lme-form
    const majicLmeForm = document.getElementById('majic-lme-form');
    if (majicLmeForm) {
      init_majicLmeForm();
      majicLmeForm.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validateLmeMajicForm()) {
          e.currentTarget.submit();
        }
      });
    }
  
    // Form for download files
    const download_form = document.getElementById('download-form');
    if (download_form !== null) {
      check_cookies();
      // INIT UUID FOR FORM EXTRACTION
      var request_id = document.getElementById('request_id').value = uuidv4();
      document.getElementById('secret').value = request_id.substring(6, 12);
      download_form.addEventListener('submit', function (e) {
        e.preventDefault();
        check_extract()
      });
    }
  });
  
  function hiddenElement(name){
    document.getElementById(name).style.display = 'None';
    }
  
  // Majic form validation
  function validateLmeMajicForm() {
    // Validation flag
    let valid = true;
    let msg_error = '';
    if( document.getElementById("fileDeclaration").files.length == 0 ){
      msg_error = '<li>Vous devez charger le document de la declaration signé.</li>';
      show_msg_error(msg_error);
      valid = false;
    }
    if( document.getElementById("fileClause").files.length == 0 ){
      msg_error = '<li>Vous devez charger le document de la clause signé.</li>';
      show_msg_error(msg_error);
      valid = false;
    }
    
    return valid;
  }
  
  function show_msg_error(msg){
    const msg_error = document.getElementById('msg-validation-error');
    msg_error.innerHTML = `<button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button>` + msg;
    $('#msg-validation-error').show();
                  
  }
  