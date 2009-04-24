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
          handle: 'h3, .word',
          /*cursorAt: {
              left: 20,
              top:  20
            },*/
          //distance: 10,
          cursor: 'move'
        })
      .bind('sortupdate', reorder)
      .bind('sortstart', function (e, ui) {
          ui.placeholder.css('height', '1.75em');
          $(this).sortable( 'refreshPositions' );
          $(this).attr('unselectable', true);
        });


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
        });

  $('h3, .word', wordCont)
      .bind('focusin click', function (e) {
          var _this = $(this).closest('fieldset'),
              _clickcausedbysort = e.type == 'click'  &&  _this.data('clickcausedbysort');

          _clickcausedbysort &&  _this.removeData('clickcausedbysort');

          if (!slideopenTimeout  &&  !_clickcausedbysort)
          {
            slideopenTimeout = setTimeout(function(){
                if (lastOpen != _this[0]) 
                {
                  lastOpen && $('.eval', lastOpen).slideUp().parent().removeClass('open');
                  $('.eval', _this).slideDown();
                  $(_this).addClass('open');
                  $('.word input', _this).trigger('focus');
                  lastOpen = _this[0];
                }
                else if ( !$(e.target).is('a, input') )
                {
                  $('.eval', _this).slideUp();
                  _this.removeClass('open');
                  $('.word input', _this).trigger('blur');
                  lastOpen = null;
                }
                slideopenTimeout = null;
              }, 400);
          }
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
        /*
          ({
              "ResultSet": {
                  "totalResultsAvailable":"4",
                  "firstResultPosition":4,
                  "Result":4,
                  "Result": [
                      {"Word": "ordeild" },
                      {"Word": "gúrka" },
                      {"Word": "ordild" },
                      {"Word": "ordna" },
                      {"Word": "ordóvísíum" }
                    ]
                }
            }).ResultSet.Result,
        */
          '/ordabok',
          {
            //minChars: 1, // 1 or 0
            //autoFill: false,
            max: 20,
            delay: 400,
            matchContains: true,
            qParam: 'sw',
            extraParams: { dbid: '2' },
            parse: function(data){
                data = (window["eval"]("("+data+")") || {}).ResultSet || {};
                var rows = data.Result || [];
                for (var i=0, word; (word = rows[i]); i++)
                {
                  word = word.Word;
                  rows[i] = { data: word,  value: word,  result: word };
                }
                return rows;
              },
            formatItem: function(row, i, max) {
                return row;
              },
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
                  valElm
                      .text( $('option[selected]', selElm).text() )
                      .attr('class', 'value value'+ui.value);
                };
          var valElm  = $('<span class="value" />').insertAfter( selElm )
          $('<span />')
              .slider({
                  //animate: true,
                  max:     maxVal,
                  min:     minVal,
                  value:   startVal
                })
              .bind('slide', changeHandler)
              .insertAfter( selElm )
              .wrap( '<span class="slider" />' );


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
