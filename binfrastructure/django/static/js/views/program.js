define([
  'ember',
  'd3',
  'app',
  'text!templates/program.handlebars'
],
function(
  Ember,
  d3,
  App,
  programHtml
) {

  App.ProgramView = Ember.View.extend({
    template: Ember.Handlebars.compile(programHtml),

    program: new Array(),

    didInsertElement: function() {
      console.log("in didIE for Program");

      // Doesn't work
      // this.addObserver('program', this, 'drawProgram');

      this.drawProgram();
    },

    drawProgram: function() {
      console.log('drawing program', this.program);
      var _this = this;
      var stepdiv = d3.select('.step_container');
      var steps = stepdiv.selectAll('.step')
        .data(this.program);

      steps.enter().append('div')
          .attr('class', 'step nonselectable')
          .on('click', function(d, i) { _this.selectStep(i); });

      steps
          .attr('index', function(d, i) { return i; })
          .text(function(d) { return d; })
          .attr('id', function(d, i) { return 'step' + i; })
          .append('span')
            .attr('class', 'deletebutton nonselectable')
            .text('[X]')
            .on('click', function(d, i) { _this.deleteStep(i); });

        steps.exit().remove();
    },

    /* ---------------------------------------------------------------------- */
    // Adding/deleting steps

    deleteStep: function(index) {
      this.program.splice(index, 1);
      // manually redraw the program; I can't get Ember observers to work
      this.drawProgram();
    },

    addStep: function(newstep) {
      this.program.push(newstep);
      console.log('new program:', this.program);

      // manually redraw the program; I can't get Ember observers to work
      this.drawProgram();
    },

    // Change which step is currently selected
    selectStep: function(index) {
      $('.selected').removeClass('selected');
      $('#step' + index).addClass('selected');
    },
  
    /* ---------------------------------------------------------------------- */
    // Specific actions

    pickup : function(evt) {
      this.addStep('Pick up from the kitchen');
    },

    dropoff: function(evt) {
      this.addStep('Drop off at Elvio\'s office');
    },

    speak: function(evt) {
      this.addStep('Say "Hello!"');
    },

    wait: function(evt) {
      this.addStep('Wait 30 seconds');
    },

    recharge: function(evt) {
      this.addStep('Recharge batteries');
    }

  });

});


