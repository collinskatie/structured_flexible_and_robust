var timeline = []

// capture info from Prolific
// help from: https://www.jspsych.org/overview/prolific/
var subject_id = jsPsych.data.getURLVariable('PROLIFIC_PID');
var study_id = jsPsych.data.getURLVariable('STUDY_ID');
var session_id = jsPsych.data.getURLVariable('SESSION_ID');

jsPsych.data.addProperties({
  subject_id: subject_id,
  study_id: study_id,
  session_id: session_id
});

// parameters to control the experimental conditions
var use_unconstrained = false;
var use_typical_constraints = true;
var num_goals = 7; // number of goals to show per participant

// extract batch of goals based on condition
// help from: https://github.com/jspsych/jsPsych/discussions/1705
var goal_batch = test_stimuli[CONDITION-1];

// keep track of shuffled goal order for consistency across phases
var goal_idxs = [];

// create a map of goals to constraints
var constraints_per_goal = {}
for (var i = 0; i < goals_with_constraints.length; i++){
	var goal = goals_with_constraints[i]["goal"]
	var typical_constraint = goals_with_constraints[i]["without typical"]
	constraints_per_goal[goal] = {"typical": typical_constraint}
}

var instructions = {
    type: "instructions",
    pages: ['<p> Welcome! </p> <p> We are conducting an experiment about how people generate plans. Your answers will be used to inform computer science and cognitive science research about planning and language. </p>' +
            '<p> This experiment should take at most <strong>30 minutes</strong>. </br></br> You will be compensated at a base rate of $15/hour for a total of <strong>$7.50</strong>, which you will receive as long as you complete the study.</p>',
                '<p> We take your compensation and time seriously! The email for the main experimenter is <strong>catwong@mit.edu</strong>. </br></br> Please write this down now, and email us with your Prolific ID and the subject line <i>Human experiment compensation for language experiment</i> if you have problems submitting this task, or if it takes much more time than expected. </p>',
                '<p> In this experiment, you will be reading descriptions of goals. Your task is to <strong>write a plan</strong>, <i>in English</i>, that someone could use to achieve each goal.</p>' +
                '<p> You will see a total of <strong>' + num_goals + '</strong> goals. For each goal, please write out <strong>one</strong> plan. </p>' +
                '<p> Some goals may be harder than others. There are no right answers. Please try your best regardless. </p>',
                '<p> You can write as much or as little is necessary to convey to someone how to achieve the goal; one or a few sentences should be a sufficient level of detail for most goals. </p>' +
                '<p> However, keep in mind that another human participant will be rating whether your plans are good or bad. You will recieve a <strong>bonus</strong> for each of your plans that gets rated as good, up to a total of <strong>$1</strong> extra.</p>',
                ],
                // '<p> When you are ready, please click <strong>\"Next\"</strong> to complete a quick comprehension check, before moving on to the experiment. </p>'],
    show_clickable_nav: true
};


var quality_control = {
    type: "survey-text",
    preamble: function() {

      instruction_text = '<p> We next ask that you please complete a quick quality control check. Data from this study will be used for research purposes, as such, low-quality data will impact our findings. We really appreciate your patience up front.</p>'

      instruction_text += '<p> You are of course welcome to write creative or risky plans to achieve each goal - there are no right answers. We only ask that you give a <i>high-quality effort</i> per goal.</p>'

      img_html_str = '<img src=\"qualityControl.png\" width=800>'

      close_text = '<p> To confirm that you understand, we ask that you <strong>type in the bolded sentences below</strong> <i>exactly as they are written</i>. Failure to do show will indicate lack of attention and will result in payment being withheld from the study. We greately appreciate you trying your best in our study!</p>'

      return instruction_text +close_text + img_html_str },
  questions: [
      {prompt: "",rows: 5, columns: 50}],
    button_label: "Next",
};
// timeline.push(quality_control)

var pre_check = {
    type: "instructions",
    pages: ['<p> When you are ready, please click <strong>\"Next\"</strong> to complete a quick comprehension check, before moving on to the experiment. </p>'],
    show_clickable_nav: true
};

var comprehension_check = {
   type: "survey-multi-choice",
        preamble: ["<p align='center'>Check your knowledge before you begin. If you don't know the answers, don't worry; we will show you the instructions again.</p>"],
        questions: [
            {prompt: "What will you be asked to generate?", options: ["Artistic doodle.", "Plans to achieve goals.", "Poems.",], required: true},
            {prompt: "How will you be providing your answer?", options: ["By writing text.", "By drawing pictures.", "Filling out a multiple choice questionnaire."], required: true},
            {prompt: "We will be checking your answers to ensure they can be used for academic research. Which of the following could impact your payment for this task?",
            options: ["Not making a good attempt to write a high-quality answer for each task.",
            "Writing creative but unusual answers for each task.",
            "Writing high-quality but risky answers for each task."], required: true},
        ],
            on_finish: function(data) {
              var responses = data.response;

              if (responses['Q0'] == "Plans to achieve goals." && responses['Q1'] == "By writing text." && responses['Q2']=="Not making a good attempt to write a high-quality answer for each task.") {
                familiarization_check_correct = true;
              }else{
                familiarization_check_correct=false;
              }
            }
}

var familiarization_timeline = [instructions, quality_control, pre_check, comprehension_check]

var familiarization_loop = {
              timeline: familiarization_timeline,
              loop_function: function(data) {
                return !familiarization_check_correct;
              }
            }

timeline.push(familiarization_loop)

var final_instructions = {
    type: "instructions",
    pages: ['<p> Now you are ready to begin! </p>' +
                '<p> Please click <strong>\"Next\"</strong> to start the experiment. Thank you for participating in our study! </p>'],
    show_clickable_nav: true
};
timeline.push(final_instructions)

var parse_goal_and_constraint = function parse_goal_and_constraint(goal, constraints){
  // if constraints is not empty, concatenate to goal
  // move end-of-sentence to end of constraint
  // for now, only use one constraint

  if (constraints == ""){
    return goal
  } else{
    constraint =  constraints.split(';')[0]
    return goal.slice(0, -1) + ' <i>' + constraint + '</i>.'
  }

}

var generate_text = {
    type: 'survey-text',
    questions: [
        {prompt: function() {
          var goal = jsPsych.timelineVariable('goal')

          // parameters to toggle between constriant-conditions
          if (use_unconstrained){
            var constraints = "" // empty constraint - just show original goal
          } else{ // o.w., pull different kinds of constraints to concat
            if (use_typical_constraints){
              var constraints = constraints_per_goal[goal]["typical"]//jsPsych.timelineVariable('constraints (w/o typical)')
            } else{
              var constraints = jsPsych.timelineVariable('constraints (w/ atypical)')
            }
          }

          return '<p><strong>My goal is to: </strong>'
          + parse_goal_and_constraint(goal, constraints) + '</p>'
          },
          rows: 5, columns: 50,
          required: true,
          placeholder: 'Enter your plan here',
          name: "Plan"
        },
    ],
    data: {
        prompt: jsPsych.timelineVariable('goal'),
        task: 'generate plans',
        constraint: function(){
          if (use_unconstrained){return "unconstrained"}
          else {
            if (use_typical_constraints){
              var goal = jsPsych.timelineVariable('goal');
              var constraints = constraints_per_goal[goal]["typical"]
              return constraints.split(';')[0] // hack!! assumes separated by ";"
            }
          }
        }
    },
    on_finish: function() {
      var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
      var prop_increase = 1/(num_goals * 2); // because 2 phase
      // var prop_increase = 1/num_goals;
      jsPsych.setProgressBar(curr_progress_bar_value + prop_increase);
    }
};


var generate_task = {
    timeline: [generate_text],
    timeline_variables: goal_batch,
    data: {
        phase: 'test'
    },

    sample: {
        type: 'custom',
          fn: function(t) {
          // t = set of indices from 0 to n-1, where n = # of trials in stimuli variable
           // returns a set of indices for trial

          // shuffle the current batch of goals
          // save order to be used again for Phase 2
          // shuffle and save that set and for use in Phase 2
          goal_idxs = jsPsych.randomization.shuffle(t)
          return goal_idxs

        }

    }
}

timeline.push(generate_task);

var phase2_instructions = {
    type: "instructions",
    pages: ['<p> You are now done with Phase 1 of the experiment</p> <p>When you are ready, please click <strong>\"Next\"</strong> to move on to the instructions for Phase 2.</p>',
            '<p> In Phase 2, you will see each of the goals again.'+
            ' Your task in this part is to <strong>rate how frequently you think people try to achieve each goal.</strong></p>'+
            '<p> For each goal, you will <strong>input your ratings using a multiple choice scale</strong>.'+
            '<p> There will be a total of <strong>'+num_goals+' goals</strong> for you to rate.</p>' +
            '<p> When you are ready, please click <strong>\"Next\"</strong> to complete a quick comprehension check, before moving on to the final stage of the experiment. </p>'],
    show_clickable_nav: true
};

var phase2_comprehension_check = {
  type: "survey-multi-choice",
        preamble: ["<p align='center'>Check your knowledge before you begin. If you don't know the answers, don't worry; we will show you the instructions again.</p>"],
        questions: [
            {prompt: "What will you be asked to rate in this task?", options: ["The goodness of plans.", "The creativity of drawings.", "How frequently you think people try to achieve each goal.",], required: true},
            {prompt: "How will you be providing your answer?",
            options: ["By selecting an option from a multiple choice scale.","By writing text.", "By moving sliders."],
            required: true},
        ],
            on_finish: function(data) {
              var responses = data.response;

              if (responses['Q0'] == "How frequently you think people try to achieve each goal." && responses['Q1'] == "By selecting an option from a multiple choice scale.") {
                familiarization_check_correct = true;
              }else{
                familiarization_check_correct=false;
              }
            }
}

var phase2_familiarization_timeline = [phase2_instructions, phase2_comprehension_check]

var phase2_familiarization_loop = {
              timeline: phase2_familiarization_timeline,
              loop_function: function(data) {
                return !familiarization_check_correct;
              }
            }

timeline.push(phase2_familiarization_loop)

var phase2_final_instructions = {
    type: "instructions",
    pages: ['<p> Now you are ready to begin the final stage of the experiment! </p>' +
                '<p> Please click <strong>\"Next\"</strong> to start the experiment.</p>'],
    show_clickable_nav: true
};
timeline.push(phase2_final_instructions)



var rating_page = {
    type: 'survey-likert',
    questions: [
        {
            prompt:function() {

            var goal = jsPsych.timelineVariable('goal')

                // parameters to toggle between constriant-conditions
                if (use_unconstrained){
                  var constraints = "" // empty constraint - just show original goal
                } else{ // o.w., pull different kinds of constraints to concat
                  if (use_typical_constraints){
                    var constraints = constraints_per_goal[goal]["typical"]//jsPsych.timelineVariable('constraints (w/o typical)')
                  } else{
                    var constraints = jsPsych.timelineVariable('constraints (w/ atypical)')
                  }
                }
                          return '<center><strong>'+parse_goal_and_constraint(goal, constraints)+'</strong></center>'

              },// '<strong>'+jsPsych.timelineVariable('goal')+'</strong>',
            labels: ["Most people do this on a daily basis.",
            "Most people do this frequently, but not daily.",
            "Most people only do this occasionally, if at all; some people never do it.",
            "Few people ever do this or try to do this during their lifetime; most people never do this.",
            "I doubt anyone I know has ever done this or tried to do something like this, but it???s possible someone has.",
            "It???s hard to imagine anyone ever trying to do this or something like this, but it could conceivably happen.",
            "I don???t see how this is even possible to do or try to do."],
            horizontal: false,
            required: true,
            name: 'freq'
        },
    ],
    randomize_question_order: false,
};

var rating_task = {
    timeline: [rating_page],
    timeline_variables: goal_batch,
    data: {
        prompt: jsPsych.timelineVariable('goal'),
        task: 'rate plans',
        constraint: function(){
          if (use_unconstrained){return "unconstrained"}
          else {
            if (use_typical_constraints){
              var goal = jsPsych.timelineVariable('goal');
              var constraints = constraints_per_goal[goal]["typical"]
              return constraints.split(';')[0] // hack!! assumes separated by ";"
            }
          }
        }
    },
    sample: {
        type: 'custom',
        fn: function (t) {
            // t = set of indices from 0 to n-1, where n = # of trials in stimuli variable
            // returns a set of indices for trials

            // use same idxs + order as phase 1
            return goal_idxs
          //return jsPsych.randomization.sampleWithoutReplacement(t,3)
        }
    },
    on_finish: function() {
      var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
      var prop_increase = 1/(num_goals * 2); // because 2 phase
      jsPsych.setProgressBar(curr_progress_bar_value + prop_increase);
    }
}

timeline.push(rating_task);

var comments_block = {
    type: "survey-text",
    preamble: "<p>Thank you for participating in our study!</p>"+
    "<p>Click <strong>\"Finish\"</strong> to complete the experiment and receive compensation. If you have any comments about Phase 1 and/or Phase 2, please let us know in the form below.</p>",
    questions: [
      {prompt: "Were the instructions clear? (On a scale of 1-10, with 10 being very clear)"},
      {prompt: "How challenging was Phase 1 of the experiment? (On a scale of 1-10, with 10 being very challenging)"},
      {prompt: "How engaging was Phase 1 of the experiment? (On a scale of 1-10, with 10 being very engaging)"},
      {prompt: "How challenging was it, in Phase 2, to imagine how often people may do these goals? (On a scale of 1-10, with 10 being very challenging)"},
      {prompt: "Do you have any additional comments to share with us?",rows: 5, columns: 50}],
    button_label: "Finish",
};
timeline.push(comments_block)


jsPsych.init({
    timeline: timeline,
    on_finish: function () {
        // send back to main prolific link
        // window.location = "https://www.google.com/"
        window.location = "https://app.prolific.co/submissions/complete?cc=4E967F29"
    },
    show_progress_bar: true,
    auto_update_progress_bar: false
});
