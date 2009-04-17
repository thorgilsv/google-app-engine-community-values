// encoding: utf-8
jQuery.noConflict();
jQuery(function($){


  $('body').addClass('js-active');
  $(':submit').each(function(){ this.value += ' >'; });
  $('form').autoValidate({
      defangEnter: true
    });


  var pwFields = $('.fi_pwd input')
      // disallow pasting into password fields
      .bind('paste', function(e){
          return false;
        })
      // enforce repeated passwords
      .bind('change', function(e){
          var pw1 = pwFields[0].value,
              pw2 = pwFields[1].value;
          if (pw1 && pw2 && pw1!=pw2)
          {
            alert('Bæði lykilorðin þurfa að vera eins!')
            var _this = $(this);
            setTimeout(function(){
                _this.trigger('focus')[0].select();
              }, 0);
          }
        });



  var agegenderOl,

      agegenderItemTempl = [
          '<li>',
            '<span class="fi_txt fi_qty req">',
              '<label for="reg_age%{i}">Aldur:</label>',
              '<input id="reg_age%{i}" type="text" name="age_%{i}" value="" maxlength="3" title="Aldur þátttakanda %{i}" />',
            '</span>',
            '<span class="fi_sel req">',
              '<label for="reg_gender%{i}">Kyn:</label>',
              '<select id="reg_gender%{i}" name="gender_%{i}" title="Kyn þátttakanda %{i}">',
                '<option></option>',
                '<option value="kvk">Kvenkyns</option>',
                '<option value="kk">Karlkyns</option>',
              '</select>',
            '</span>',
          '</li>'
        ].join('\n'),
      
      displAgegenderFields = function(e){
          var _this = $(this);
              _val = parseInt( '0'+_this.val(), 10);
          if (agegenderOl || _val)
          {
            if (!agegenderOl)
            {
              var agegenderFs = $([
                  '<fieldset class="agegender">',
                  '  <h3><acronym class="req" title="Þarf að fylla út: ">*</acronym>Þátttakendur:</h3>',
                  '  <ol>',
                  '  </ol>',
                  '</fieldset>'].join('\n')
                );
              $(this).closest('.fi_sel').after(agegenderFs);
              $('.fi_qty input').live('keypress', function(e){
                  var key = e.which;
                  return (
                      // Allow:
                      !key ||    //most passive keystrokes (including arrow keys)
                      key==8  || //(backspace (at least in some browsers)
                      (key>=48  &&  key<=57) // 0-9 digits
                    ); 
                });
              agegenderOl = $('ol', agegenderFs);
            }
            var numLis = agegenderOl.children().length,
                added = false;

            for (var i=numLis; i<_val; i++) {
              agegenderOl.append(
                  agegenderItemTempl.replace(/%{i}/g, i)
                );
              added = true;
            }
            if (!added)
            {
              $('> *:gt('+(_val-1)+')', agegenderOl).remove();
            }
          }
        };


  var numPplSelect = $('.num_ppl select').bind('change', displAgegenderFields);
  displAgegenderFields.call(numPplSelect); // initialize the ageGender fields



});
