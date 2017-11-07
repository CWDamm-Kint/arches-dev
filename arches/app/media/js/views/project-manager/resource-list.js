define([
    'knockout',
    'arches',
    'views/list'
], function(ko, arches, ListView) {
    var ResourceList = ListView.extend({
        /**
        * A backbone view to manage a list of graph nodes
        * @augments ListView
        * @constructor
        * @name ResourceList
        */

        single_select: true,

        /**
        * initializes the view with optional parameters
        * @memberof ResourceList.prototype
        * @param {object} options
        * @param {boolean} options.permissions - a list of allowable permissions
        * @param {boolean} options.card - a reference to the selected {@link CardModel}
        */
        initialize: function(options) {
            ListView.prototype.initialize.apply(this, arguments);
            var self = this;
            this.items = options.items;

            _.each(this.items(), function(item){
                item.cards = ko.observableArray(item.cards);
                _.each(item.cards(), function(card){
                    card.approved = ko.observable(false);
                    card.expanded = ko.observable(false);
                    card.widgetlabels = _.map(card.widgets, function(w) {return w.label}).join(', ');
                })
            })

            this.selected = ko.computed(function(){
                var res = self.selectedItems().length > 0 ? self.selectedItems()[0] : '';
                return res;
            })
        }

    });
    return ResourceList;
});
