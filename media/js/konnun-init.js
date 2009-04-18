// encoding: utf-8
jQuery.noConflict();
jQuery(function($){


  $('body').addClass('js-active');
  $(':submit').each(function(){
      if ($(this).closest('.back').length)
      {
        this.value = '< '+this.value;
      }
      else
      {
        this.value += ' >';
      }
    });


  var UP = 38,
      DOWN = 40,

      moverBtns = $('<div class="mover">'+
                       '<a href="#" class="up" title="Færa framar í forgangsröð">Upp</a> '+
                       '<a href="#" class="dwn" title="Færa aftar í forgangsröð">Niður</a>'+
                    '</div>')
        /*
        .bind('keydown', function(e){
            if (e.which == DOWN  || e.which == UP )
            {
              moveWord( e.target,  e.which==UP );
            }
          })
        */
        .bind('click', function(e){
            var targ = e.target;
            if (targ.tagName == 'A')
            {
              moveWord( targ, targ.className=='up' );
            }
            e.stopPropagation();
          }),


      moveWord = function (elm, moveUp) {
            var fieldset = $(elm).closest('fieldset'),
                method = moveUp ?
                            { find:'prev',  insert:'insertBefore' }:
                            { find:'next',  insert:'insertAfter' },
                siblingFs = fieldset[method.find]();

            if (siblingFs.length)
            {
              fieldset[method.insert]( siblingFs );
              $(elm).trigger('focus');
            }
            reorder();
        },

      reorder = function (e, ui) {
          $('> fieldset', wordCont)
              .each(function(i){
                  var order = i+1;
                  $('h3', this).text( order );
                  $('.order input', this).val( order );
                });
        },


      wordCont = $('div.words');


  wordCont
      .attr('type', '1')
      .sortable({
          handle: 'h3, .word, .mover',
          cursor: 'move',
          /*cursorAt: {
              left: 20,
              top:  20
            },*/
          distance: 10
        })
      .bind('sortupdate', reorder);

  wordCont.closest('form')
      .bind('keydown', function(e){
          var target = e.target;
          return ( e.which != 13  ||  target.tagName != 'INPUT'  ||  /^(button|reset|submit)$/i.test(target.type) );
        });


  var lastOpen,
      slideopenTimeout;

  $('> fieldset', wordCont)
      .each(function(i){
          $(this)
            .prepend( moverBtns.clone(true) )
            .prepend( '<h3>'+ (i+1) +'</h3>');
        })
      .bind('focusin click', function(e){
          var _this = this;
          clearTimeout(slideopenTimeout);
          slideopenTimeout = setTimeout(function(){
              if (lastOpen != _this) 
              {
                lastOpen && $('.eval', lastOpen).slideUp().parent().removeClass('open');
                lastOpen = _this;
                $('.eval', _this).slideDown();
                $(_this).addClass('open');
              }
            }, 400);
        });


  $('.word input', wordCont)
      .bind('keypress', function (e) {
          return e.which != 32;
        })
      .bind('change', function (e) {
          var value = this.value,
              i = value.length,
              errMsg;
          if (/\s/.test(value))
          {
            errMsg = 'Vinsmlega sláðu bara inn eitt orð í hvern reit';
          }
          else
          {
            while (i--)
            {
              var chr = value.charAt(i);
              if ( chr.toUpperCase() != chr.toLowerCase()  &&  chr != '-' )
              {
                errMsg = 'Vinsamlega notaðu bara venjulega bókstafi';
                break;
              }
            }
          }
          if (errMsg)
          {
            var _this = $(this);
            setTimeout(function(){
                _this.trigger('focus')[0];
              }, 0);
          }

        })
      .autocomplete(
          '/ordabok',
          //'Indíukirsuber,Epli,Apríkósur,Asískar perur,Lárperur,Banani,Bananamelónur,Bláber,Brómber,Brauðávöxtur,Kaktusfíkja,Stjörnuávöxtur,Kirsuber,Trönuber,Rifsber,Sólber,Morgunberkja,Döðlur,Blá hindber,Drekaávöxtur,Dáraaldin,Ylliber,Fíkjur,Garðaber,Stikilsber,Greipaldin,Guava,Hunangs melóna,Saðningaraldin,Jujube,Kantalúpmelónur,Kívanó,Kíví (loðber),Dvergappelsína,kúmkvat,Sítrónur,Súraldin;límónur,Litkaber,Loganber,Longan,Dúnepli,Loquat,Mandarínur,Mangó,Mangosteen,Svört mórber,Nektarínur,Ólífur,Appelsínur,Appelsínur beiskar,Papaja,Ástaraldin,Píslaraldin,Ferskjur,Perur,Pepino,Döðluplóma,Mjölbananar,Plómur,Ananas,Pómelóaldin,Granatepli,Kveði,Rúsínur,Rambútan,Hindber,Jarðaber,Vínber,Tamarind,Tamarillo,Ugli,Vatnsmelónur,Grænmeti og fl.,Akorn grasker,Túnætisveppur,Spergill,Aspas,Eggaldin,Rauðrófur,Blaðbeðja (strandblaðka),Blue hubbard grasker,Kóngssveppur,Spergilkál,Rósakál,Buttercup grasker,Barbapabba grasker,Hvítkál,Fingrakornblóm,Carnival grasker,Gulrætur,Blómkál,Hnúðselja,sellerírót,Stilkselja,Sellerí,Ætisveppur,Kínakál,Kúrbítur af graskeraættDvergbítur,Agúrkur,Delicata grasker,Vetrarsalat,Fennika(sígóð),Hvítlaukur,Þrúgugúrkur,Ætiþistill,Höfuðkál,Humall,Piparrót,Íssalat,Ætifífill,Grænkál,Hnúðkál,Blaðlaukur,Laukur,Nípa,Steinseljurót,Paprikur,Kartöflur,Pumpkin grasker,Hreðkur (radísur),Red kuri grasker,Red turban grasker,Rabarbari,Hafursrót,Skalottlaukur (askalonlaukur),Spagettí grasker,Spínat,Perlulaukur,Maís,Korn,Maískólfar,Sætuhnúðar,sætar kartöflur,Gulrófur,Sweet dumpling grasker,Tómatar,Næpur,Kínakartöflur,Kryddjurtir,Kerfill,Graslaukur,Blaðselja,Karsi (garðperla),Vatnakarsi,Vorsalat,Steinselja,Jólasalat,Hnetur,Möndlur,Brasilíuhnetur,Kasúhnetur,Kastaníu hnetur,Kókoshnetur,Heslihnetur,Makademía hnetur,Pekan hnetur,Jarðhnetur,Furu hnetur,Pistasíu hnetur (hjartaaldin),Valhnetur,Krydd,Kúmenfræ,Einiber,Múskat,Pipar svartur og hvítur,Vanillufræ,Fræ,Baðmullarfræ,Hörfræ,Sinnepsfræ,Ertur (án fræbelgs),Ertur (með fræbelg),Valmúafræ (birki),Repjufræ,Sesamfræ,Sólblómafræ,Baunir,Rauðar nýrnabaunir,Adúkí baunir,Anasasí baunir,Boston baunir,Kjúklingabaunir,Fava baunir,Límabaunir,Smjörbaunir,Pintó baunir,Sojabaunir'.split(','),
          {
            //minChars: 1, // 1 or 0
            //autoFill: false,
            max: 20,
            delay: 400,
            matchContains: true,
            qParam: 'sw',
            extraParams: { dbid: '2' },
            scrollHeight: 220
          }
        );


  $('.eval select', wordCont)
      .hide()
      .each(function(i){
          var selElm = $(this),
              maxVal = $('option[value]', selElm).length,
              minVal = 1,
              startVal = selElm.val() || Math.ceil( (maxVal+minVal)/2 ),
              changeHandler = function (e, ui) {
                  selElm.val( ui.value );
                  valElm.text( $('option[selected]', selElm).text() );
                };
          var valElm  = $('<span class="value" />').insertAfter( selElm )
          $('<span />')
              .slider({
                  //animate: true,
                  max:     maxVal,
                  min:     minVal,
                  value:   startVal
                })
              .bind('slidechange', changeHandler)
              .insertAfter( selElm );


          changeHandler(null, { value: startVal });
        })
      .parent().find('label')
          .bind('click', function(e){
              $('a.ui-slider-handle', this.parentNode).trigger('focus'); return false;
            });


    var maxWords = parseInt( $('.fi_bdy label i', wordCont).text().replace(/\D/, ''), 10);
    ;;;window.console&&console.log( 'Max words: ', maxWords );
    if (!isNaN(maxWords))
    {
      $('textarea', wordCont)
          .bind('change', function(e){
              var inpElm = $(this),
                  value = $.trim( inpElm.val() ),
                  numWords = value.split(/\s/).length;
              inpElm
                  .val( value )
                  .removeClass('invalid');
              if ((numWords + value.length/5)/2 > maxWords) // Compare the average of word-count and word-estimation to the max number of words allowed.
              {
                alert('Vinsamlega reynið að halda athugasemdum stuttum og hnitmiðuðum.');
                setTimeout(function(){
                    inpElm
                        .addClass('invalid')
                        .trigger('focus');
                  }, 0);
              }
            });
    }


});
