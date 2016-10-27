
/*
function setHighlight (word, mode) 
{
   if (mode) word.className = "word highlighted"; 
        else word.className = "word nothighlighted";
}
*/

function setHighlight (word, mode) 
{
   if (mode) $(word).addClass("highlighted");
      else   $(word).removeClass("highlighted");
}

//makes a list of all spans (list of js objects) of all variants of a paragraph
function preprocessFragments (fragments) {
  var words= new Array ();
  for (key in fragments) {
      var words_part = $('#'+fragments[key]+' .word') 
      for(var i = 0; i < words_part.length; i++) 
          words.push(words_part[i]);
  }

return words;
}

function preprocessConnections (fragments, connections, lang_keys) {//so far preprocesses only connections
  
  var preprocessed_connections={};
  for (group_array_no in connections) {
      group_array=connections[group_array_no];
      for (var i = 0; i < lang_keys.length; i++) {
        small_array=group_array[lang_keys[i]];
          for (word_id in small_array) {
               frag_id=document.getElementById(fragments[lang_keys[i]]).getAttribute("id");
               word_id_full=frag_id+"w"+small_array[word_id];
               preprocessed_connections[word_id_full]=connections[group_array_no];
           }
       }

    }
   return preprocessed_connections;
}


function changeGroupColor(word_id, prep_connections, fragments, words, lang_keys) 
 {
    for (var i in words) setHighlight(words[i], false);
        
    var connected_words=prep_connections[word_id];
//console.log(JSON.stringify(prep_connections));
    for (var i = 0; i < lang_keys.length; i++) {
         var key=lang_keys[i];
         var p_id=document.getElementById(fragments[key]).getAttribute("id");
         var small_array=connected_words[key];

         for (word_key in small_array) {
              var w_number=small_array[word_key];
              var w_id=p_id+"w"+w_number;
              setHighlight (document.getElementById(w_id), true);
         }   
    }
    
 }

$(document).ready(function(){
    $.ajax({ 
     url:root+text_name+'/get_fragments_and_connections.json',//this is route from the root of the site
     dataType:'json'
    })
    .done(function(data) {//method .done. its parameter is function whose par.is data that came in response to ajax request
     for (var j=0;j<data.length;j++) { 
     (function (frag_data) {

     var fragments=frag_data.fragments;

     var connections=frag_data.connections;
     var lang_keys=frag_data.lang_keys;
     var fragment_id=frag_data.fragment_id;
     var words=preprocessFragments(fragments);
//console.log(JSON.stringify(connections));
     var preprocessed_connections=preprocessConnections (fragments,connections, lang_keys);
console.log("PREPROCESSED_CON"+JSON.stringify(preprocessed_connections))
     for (var i=0;i<words.length;i++) 
     {
       var w = words[i];
       w.onclick=function () { word_id=this.getAttribute("id"); 
                                changeGroupColor(word_id,preprocessed_connections, fragments,words, lang_keys);
                                 if ("_comment" in preprocessed_connections[word_id])
                                    var comment=preprocessed_connections[word_id]["_comment"];
                                 else
                                    comment='';
                                 $("#"+fragment_id+" .comment").html(comment);   
          }
     }
     }) (data[j]);
    }
    });
});


//closure - if there aretwo anonymous functions, one inside the other. inner function can refer to the local var of outer function. in such a case, the local variables of outer function continue living even after it stopped its work and the inner f can use them whenever it is called or even change them


 


