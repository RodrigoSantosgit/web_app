$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: '',
            center: 'title',
            right: 'agendaWeek,agendaDay'
        },
        weekends: false,
        defaultView: 'agendaWeek',
        events: [
		/*{% for e in events %}
		{ 
			title:"{{ e.name }}",
			start:"{{ e.Start_date }}",
			end:"{{ e.End_date }}",
			id:"{{ e.id }}",
		},
		{% endfor %}*/
	
	],
        eventAfterAllRender: function() {

            // define static values
            var defaultItemHeight = 45;
            var defaultEventItemHeight = 40;
            // ...

            // find all rows and define a function to select one row with an specific time
            var rows = [];
            $('div.fc-slats > table > tbody > tr[data-time]').each(function() {
                rows.push($(this));
            });
            var rowIndex = 0;
            var getRowElement = function(time) {
                while (rowIndex < rows.length && moment(rows[rowIndex].attr('data-time'), ['HH:mm:ss']) <= time) {
                    rowIndex++;
                }
                var selectedIndex = rowIndex - 1;
                return selectedIndex >= 0 ? rows[selectedIndex] : null;
            };

            // reorder events items position and increment row height when is necessary
            $('div.fc-content-col > div.fc-event-container').each(function() { // for-each week column
                var accumulator = 0;
                var previousRowElement = null;

                $(this).find('> a.fc-time-grid-event.fc-v-event.fc-event.fc-start.fc-end').each(function() { // for-each event on week column
                    // select the current event time and its row
                    var currentEventTime = moment($(this).find('> div.fc-content > div.fc-time').attr('data-full'), ['h:mm A']);
                    var currentEventRowElement = getRowElement(currentEventTime);

                    // the current row has to more than one item
                    if (currentEventRowElement === previousRowElement) {
                        accumulator++;

                        // move down the event (with margin-top prop. IT HAS TO BE THAT PROPERTY TO AVOID CONFLICTS WITH FullCalendar BEHAVIOR)
                        $(this).css('margin-top', '+=' + (accumulator * defaultItemHeight).toString() + 'px');

                        // increse the heigth of current row if it overcome its current max-items
                        var maxItemsOnRow = currentEventRowElement.attr('data-max-items') || 1;
                        if (accumulator >= maxItemsOnRow) {
                            currentEventRowElement.attr('data-max-items', accumulator + 1);
                            currentEventRowElement.css('height', '+=' + defaultItemHeight.toString() + 'px');
                        }
                    } else {
                        // reset count
                        rowIndex = 0;
                        accumulator = 0;
                    }

                    // set default styles for event item and update previosRow
                    $(this).css('left', '0');
                    $(this).css('right', '7px');
                    $(this).css('height', defaultEventItemHeight.toString() + 'px');
                    $(this).css('margin-right', '0');
                    previousRowElement = currentEventRowElement;
                });
            });

            // this is used for re-paint the calendar
            $('#calendar').fullCalendar('option', 'aspectRatio', $('#calendar').fullCalendar('option', 'aspectRatio'));
        }
    });

});
