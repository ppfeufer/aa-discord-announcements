/* global discordAnnouncementsSettings */

$(document).ready(() => {
    'use strict';

    /* Variables
    --------------------------------------------------------------------------------- */
    // Selects
    const selectAnnouncementTarget = $('select#id_announcement_target');
    const selectAnnouncementChannel = $('select#id_announcement_channel');

    // Input fields
    const inputCsrfMiddlewareToken = $('input[name="csrfmiddlewaretoken"]');

    // Form
    const announcementForm = $('#aa-discord-announcements-form');

    /* Functions
    --------------------------------------------------------------------------------- */
    /**
     * Get the additional Discord ping targets for the current user
     */
    const getAnnouncementTargetsForCurrentUser = () => {
        $.ajax({
            url: discordAnnouncementsSettings.url.getAnnouncementTargets,
            success: (data) => {
                $(selectAnnouncementTarget).html(data);
            }
        });
    };

    /**
     * Get webhooks for current user
     */
    const getWebhooksForCurrentUser = () => {
        $.ajax({
            url: discordAnnouncementsSettings.url.getAnnouncementWebhooks,
            success: (data) => {
                $(selectAnnouncementChannel).html(data);
            }
        });
    };

    /**
     * Closing the message
     *
     * @param {string} element
     * @param {int} closeAfter Close Message after given time in seconds (Default: 10)
     */
    const closeMessageElement = (element, closeAfter = 10) => {
        $(element).fadeTo(closeAfter * 1000, 500).slideUp(500, () => {
            $(this).slideUp(500, () => {
                $(this).remove();
            });
        });
    };

    /**
     * Show message when copy action was successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showSuccess = (message, element) => {
        $(element).html(
            '<div class="alert alert-success alert-dismissable alert-message-success">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
        );

        closeMessageElement('.alert-message-success');
    };

    /**
     * Show message when copy action was not successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showError = (message, element) => {
        $(element).html(
            '<div class="alert alert-danger alert-dismissable alert-message-error">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
        );

        closeMessageElement('.alert-message-error', 9999);
    };

    /* Events
    --------------------------------------------------------------------------------- */
    /**
     * Generate announcement text
     */
    announcementForm.submit((event) => {
        // Stop the browser from sending the form, we take care of it
        event.preventDefault();

        // Close all possible form messages
        $('.aa-discord-announcements-form-message div').remove();

        // Get the form data
        const formData = announcementForm.serializeArray().reduce((obj, item) => {
            obj[item.name] = item.value;

            return obj;
        }, {});

        $.ajax({
            url: discordAnnouncementsSettings.url.createAnnouncement,
            type: 'post',
            data: formData,
            headers: {
                'X-CSRFToken': inputCsrfMiddlewareToken.val()
            },
            success: (data) => {
                if (data.success === true) {
                    $('.aa-discord-announcements-no-announcement').hide('fast');
                    $('.aa-discord-announcements-announcement').show('fast');

                    $('.aa-discord-announcements-announcement-text').html(data.announcement_context);

                    if (data.message) {
                        showSuccess(
                            data.message,
                            '.aa-discord-announcements-form-message'
                        );
                    }
                } else {
                    if (data.message) {
                        showError(
                            data.message,
                            '.aa-discord-announcements-form-message'
                        );
                    } else {
                        showError(
                            'Something went wrong, no details given.',
                            '.aa-discord-announcements-form-message'
                        );
                    }
                }
            }
        });
    });

    /**
     * Initialize functions that need to start on load
     */
    (() => {
        getAnnouncementTargetsForCurrentUser();
        getWebhooksForCurrentUser();
    })();
});
