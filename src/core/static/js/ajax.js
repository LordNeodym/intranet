function saveTimeForSubject(evt, subjectInfos, cellInfos){
    evt.preventDefault();
 
    var newInfos = $.ajax({
        url : "/save_new_time",
        type : "GET",
        dataType: "json",
        async: true,
        data: {
            subjectDay: subjectInfos[0],
            subjectID: subjectInfos[1],
            subjectType: subjectInfos[2],
            date: subjectInfos[3],
            subjectTime: subjectInfos[4],
            subjectDuration: subjectInfos[5],
            room: subjectInfos[6],
            lecturer: subjectInfos[7],
            borderColor: subjectInfos[8],
            uid: subjectInfos[9],
            cellWidthUnits: cellInfos[0],
            cellHeightUnits: cellInfos[1],
            startTime: startTime
        },
        success : function(resp) {
            if (resp.success == true) {
                display_saveInfo("Erfolgreich gespeichert!");
                if (!$.isEmptyObject(resp.msg)) {
                    errorHandler(resp.msg);
                    $(".subject-overlay[data-subject-id='"+resp.sub_id+"']").attr("data-subject-duration", resp.duration);
                }
            } else {
                display_saveInfo("Fehler");
            }
        },
        error : function(xhr,errmsg,err) {
            display_saveInfo("Verbindung getrennt!");
        }
    });
    return newInfos
}