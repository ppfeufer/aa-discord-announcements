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

    /* Functions
    --------------------------------------------------------------------------------- */
    /**
     * Get the additional Discord ping targets for the current user
     */
    const getPingTargetsForCurrentUser = () => {
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
     * Initialize functions that need to start on load
     */
    (() => {
        getPingTargetsForCurrentUser();
        getWebhooksForCurrentUser();
    })();
});
