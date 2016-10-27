
function setHighlight (word, mode) 
{
//console.log(mode);
if (mode) 
{word.className="highlighted";} 
else 
 word.className=
"nothighlighted"
}


function get_words_id_list(fragments)
{
   var res = new Array();
   for (key in fragments)
   {
       pid=fragments[key]; 
       words = $('#'+pid+' .word').toArray()
       for (word in words) 
       {
          res.push($(words[word]).attr('id'))
       }
   }
   return res;
} 

function preprocessConnections (fragments, connections, ids_list, lang_keys) {//so far preprocesses only connections
  
  var preprocessed_connections={};
  for (word_id in ids_list) {
       preprocessed_connections[ids_list[word_id]]='nothing';
     }
  for (var i=0; i<connections.length; i++) {
      group_array=connections[i];
      for (var j=0; j < lang_keys.length; j++) {
        small_array=group_array[lang_keys[j]];
        for (word_id in small_array) {
           frag_id=fragments[lang_keys[j]];
           word_id_full=frag_id+"w"+small_array[word_id];
           preprocessed_connections[word_id_full]=i;//make group array number a number and not a string
        }
      }

    }
   
   return preprocessed_connections;
}


function backPreprocessConnections (connections, preprocessed_connections, lang_keys) {
       new_connections=[];
       max_key=0;
       for (word_full_id in preprocessed_connections) {
         if (preprocessed_connections[word_full_id]!='nothing') {
           key=preprocessed_connections[word_full_id];
           if (key>max_key) max_key=key; 
         }
       }
       //console.log(max_key); 
       for (var i=0; i<=max_key; i++) {
           pattern_for_group={};
           for (var j=0; j<lang_keys.length; j++) {
              pattern_for_group[lang_keys[j]]=[];
           }
           new_connections[i]=pattern_for_group;
        
       }
       //console.log(new_connections);
       for (word_full_id in preprocessed_connections) {
         if (preprocessed_connections[word_full_id]!='nothing') {
           var parsed_word_id=parse_word_full_id (word_full_id);
           var word_lang=parsed_word_id['lang'];
           var word_id=parseInt(parsed_word_id['id']);
           //console.log(word_full_id)
           var key=Number(preprocessed_connections[word_full_id]);
           //console.log(key);
           new_connections[key][word_lang].push(word_id); 
         }
       }
       for (var z=0; z<new_connections.length; z++) {
         //console.log(z);
         //console.log(connections);   
         if ((z<connections.length)&&("_comment" in connections[z])) 
            new_connections[z]["_comment"]=connections[z]["_comment"];
         else
            new_connections[z]["_comment"]="";
         }
       return new_connections;

}

function group_exists(preprocessed_connections, selected_group_number) {
   var flag=false;
   for (word_id in preprocessed_connections)
      if (preprocessed_connections[word_id]==selected_group_number)
          flag=true;
   return flag;
      
    }

function compare_objects (first_obj, second_obj) {
   return JSON.stringify(first_obj)==JSON.stringify(second_obj);
     }

function clone (object) {
   object_string=JSON.stringify(object);
   clone_object=$.parseJSON (object_string);
   return clone_object;
}

/* $("button").click(function(){ example of actions done as result of button click
    $("p").removeClass("intro");
});
*/

function parse_word_full_id(full_id)
{
  var re = new RegExp('([A-Za-z_]+)[0-9]*w([0-9]+)');
  var m = re.exec(full_id);
  res = new Array();

  res['lang']= m[1];
  res['id'] = m[2];

  return res;
}



function Screen(list_of_words_ids) {//this is virtual DOM.this is intermediary between the program and DOM.through this we say whhat must be on the screen. how to do this decides this object, basing on what is on the screen now.later this class will be responsible for colouring too, for all the output
   this.buttons_states={"#edit_button": "enabled", "#save_button": "enabled", "#new_button": "enabled", "#read_mode": "enabled", "#edit_text": "enabled"};
   this.comment_editor_visible=false;   
   this.comment_static_text = false;
   this.saved_comment = false;

   this.enableButton = function (button_id) {
      if (this.buttons_states[button_id]=="disabled") {
        this.buttons_states[button_id]="enabled";
        $(button_id).removeClass("disabled_button");
        }
      }
   this.disableButton = function (button_id) {
      if (this.buttons_states[button_id]=="enabled") {
        this.buttons_states[button_id]="disabled";
        $(button_id).addClass("disabled_button");
      }
   }
   
   this.words_id_list=list_of_words_ids;
   

   this.words_states_array={};
   for (key in this.words_id_list) {
      var word_full_id=this.words_id_list[key]
      this.words_states_array[word_full_id]='nothighlighted_read word';
      //console.log(word_full_id);
      document.getElementById(word_full_id).className='nothighlighted_read word';//remake in jquery later
    }
    this.comments=
       function(mode) {
         if (mode=='read') $("#comments").html('<div class="comments">Please select the group you want to edit and click <b>Edit Group</b> <br>or <br> To create new connections group click <b>New Group</b></div>'); 
         if (mode=='edit') $("#comments").html('<div class="comments"> Click on the words you want to add/remove from the group</div>'); 
       }

    this.comments ('read');

    this.show_comment_editor = function () {
       if (!this.comment_editor_visible ) {
          $(".comment").html('Comment to this group:<br><br><textarea id="comment_editor" name="comment">'+this.comment_editor_text+'</textarea>'); 
          console.log('textarea');
          var editor = $("#comment_editor").cleditor();//enables text editor
          this.comment_editor_visible = true;
          var scr = this
          editor.change(function() 
              { 
                scr.comment_editor_text = this.$area.context.value;  // to check in all browsers!!! 
                //console.log(this.comment_editor_text);
                if (scr.saved_comment != scr.comment_editor_text ) 
                {
                   scr.enableButton("#save_button");
                } else {
                   scr.disableButton("#save_button");
                }
              } );
          this.comment_static_text = false;
       }
       
    }

    this.show_comment = function (comment_text) {
       if (!this.comment_static_text || (this.comment_static_text != comment_text)) {
          $(".comment").html(comment_text); 
          this.comment_editor_text = false
          this.comment_editor_visible = false
          this.comment_static_text = comment_text;
       }
    }

   this.show_on_screen=
     function (preprocessed_connections,cloned_preprocessed_connections,connections,selected_group_number,state,selected_group) {
        if (state=='read') {   
           
          for (word_id in preprocessed_connections) {
           //console.log(preprocessed_connections[word_id]);
            if ((preprocessed_connections [word_id]==selected_group_number)&&selected_group) 
              this.wordHighlight(word_id, "highlighted");

            else
              this.wordHighlight(word_id, "nothighlighted_read");
          }
          this.enableButton("#new_button");
          this.enableButton("#edit_text");
          this.disableButton("#read_mode");
          this.comments('read');
  
          $(".text").removeClass("editing");
          //console.log(selected_group_number); 
          //console.log(connections[selected_group_number]);
   
          if ((selected_group_number != 'nothing') && (selected_group_number<connections.length)&&("_comment" in connections[selected_group_number])) 
             var comment= connections[selected_group_number]['_comment'];
          else 
             comment= '';
          this.show_comment(comment)
     }
      else {
        for (word_id in cloned_preprocessed_connections) {        
          if ((cloned_preprocessed_connections [word_id]==selected_group_number)&&selected_group) 
            this.wordHighlight(word_id, "highlighted");
          else
            this.wordHighlight(word_id, "nothighlighted_edit");
         }
         this.disableButton("#new_button");
         this.disableButton("#edit_text");
         this.enableButton("#read_mode");
         this.comments('edit');
         $(".text").addClass("editing");
         if (!this.comment_editor_visible) { 
            if ((selected_group_number<connections.length)&&("_comment" in connections[selected_group_number])) 
               this.comment_editor_text = connections[selected_group_number]['_comment'];
            else 
               this.comment_editor_text= '';

            this.saved_comment = this.comment_editor_text;  
         }
         
         this.show_comment_editor ();
                
      }
     
  //edit_button
  if ((selected_group)&&(state=='read'))
    this.enableButton("#edit_button");
  else
    this.disableButton("#edit_button");

  //save_button
  if ((state=='edit') && (selected_group) &&
      (!compare_objects(preprocessed_connections, cloned_preprocessed_connections) ||
      (this.saved_comment != this.comment_editor_text ))) 
  {
     this.enableButton("#save_button");
  }
  else {
    this.disableButton("#save_button");
  }
  
  }
   
  this.wordHighlight=function (word_id, highlight_mode) {
     if (highlight_mode!=this.words_states_array[word_id]) {
        //console.log(this.words_states_array[word_id]);
        this.words_states_array[word_id]=highlight_mode;
        document.getElementById(word_id).className=highlight_mode+" word";
      }
       
   }
}

function Automaton (connections_of_fragment_versions, screen, fragments, lang_keys) {//creates an object when we call it with 'new'
  this.state='read';
  this.selected_group=false;
  this.selected_group_number=0;
  this.fragments=fragments;
  this.connections=connections_of_fragment_versions;
  this.lang_keys=lang_keys;
  this.preprocessed_connections=preprocessConnections(this.fragments,this.connections,get_words_id_list(this.fragments),this.lang_keys);
  this.cloned_preprocessed_connections=clone(this.preprocessed_connections);
  this.output=screen;
  this.output.disableButton("#save_button");
  this.output.disableButton("#read_mode");
  this.output.disableButton("#edit_button");
  this.output.enableButton("#new_button");
  this.output.enableButton("#edit_text");
  this.do_action= function (action, word_full_id) {
  
   switch (this.state) {
   
      case "read":
       
       switch (action) {

          case 'word_click':
            
            this.selected_group_number=this.preprocessed_connections[word_full_id];
            this.selected_group=(this.preprocessed_connections[word_full_id]!='nothing');        
            
     
          break;

          case 'edit_button_click':
           this.state='edit';
          break;

          case 'save_button_click':
          break;

          case 'new_button_click':
           this.state='edit';
           var max_group_number=0;
           for (word_full_id in this.cloned_preprocessed_connections) {
              if (this.cloned_preprocessed_connections[word_full_id]!='nothing') {
                 var group_number=this.cloned_preprocessed_connections[word_full_id];     
                 if (group_number>max_group_number) max_group_number=group_number;
              }
           }
           this.selected_group=true;
           this.selected_group_number=max_group_number+1;
           //console.log(this.selected_group_number);
           break;

          case 'read_mode_click':
          break;

          
        }
      break;

      case "edit":
        switch (action) {

          case 'word_click':
            
            if (this.cloned_preprocessed_connections[word_full_id]==this.selected_group_number) {//if in group
               if (this.preprocessed_connections[word_full_id]==this.cloned_preprocessed_connections[word_full_id])//if was in gr befr
                 this.cloned_preprocessed_connections[word_full_id]='nothing';
               else
                 this.cloned_preprocessed_connections[word_full_id]=this.preprocessed_connections[word_full_id];
             }
            else
                this.cloned_preprocessed_connections[word_full_id]=this.selected_group_number;



           
          case 'edit_button_click':
          break;

          case 'save_button_click':
            this.preprocessed_connections=clone(this.cloned_preprocessed_connections);
            this.connections = backPreprocessConnections(this.connections, this.cloned_preprocessed_connections,this.lang_keys);
            if (this.selected_group_number < this.connections.length)
               this.connections[this.selected_group_number]['_comment'] = screen.comment_editor_text;
            $.post('save_connections',
                   {connections: JSON.stringify(this.connections)},
                   function(result){}) 
            this.state='read';
          break;

          case 'new_button_click':
          break;

          case 'read_mode_click':
           this.state='read';
           if (!group_exists(this.preprocessed_connections, this.selected_group_number)) {
              this.selected_group=false;
              this.selected_group_number=0;
           }
          break;

        } 

     }


   this.output.show_on_screen (this.preprocessed_connections, this.cloned_preprocessed_connections, this.connections , this.selected_group_number,   
                           this.state, this.selected_group);//maybe later make an array called state which will include all these parameters as its items


 }
}

var automaton=''




$(document).ready(function(){
    $.ajax({ 
     url:'data.json',
     dataType:'json'
    })
    .done(function(data) {//method .done. its parameter is function whose par.is data that came in response to ajax request
    
     
     var words_id_list=get_words_id_list(data.fragments);

     var screen = new Screen (words_id_list);
     //console.log(screen);
      automaton = new Automaton (data.connections, screen, data.fragments, data.lang_keys);

     $("#edit_button").click (function() {automaton.do_action("edit_button_click", 0);});

     $("#save_button").click (function() {automaton.do_action("save_button_click", 0);});

     $("#new_button").click (function() {automaton.do_action("new_button_click", 0);});

     $("#read_mode").click (function() {automaton.do_action("read_mode_click", 0);});

     $("#edit_text").click (function() {

        if ((automaton.connections.length==0) || 
            (confirm ( 'Editing this text will lead to the loss of all existing connections for this fragment.'
                      +'\n\nDo you want to proceed?'))) 
        {
            window.location.assign ("edit_fragment_text.html");
        }

     });

     $(".word").click (function() {
                                automaton.do_action("word_click", $(this).attr("id"));
                              });

    
    });
});

