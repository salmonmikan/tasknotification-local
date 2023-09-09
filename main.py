import get_manaba
import google_calender

def main():#data,contextはGCP用の空の関数。
    report_list = get_manaba.get_manaba_report()

    google_calender.calender_API_get()

    events_check = google_calender.calender_event_get()

    result = []
    for report_title,class_name, deadline in report_list:
        # 重複して予定を登録しないようにする
        summary_name = report_title + "/" + class_name
        if  summary_name not in events_check:
            google_calender.calender_event_insert(report_title, class_name, deadline)
            result.append((report_title, class_name, deadline))
            ###calenderから取得した予定は現在の時刻以降の予定しかないが、manabaの課題上に過去が期限の未提出課題が残っていると、元のcalenderからは予定を取得していないために重複確認で見過ごされて無限に登録されてしまう。修正予定。→過去の予定もまとめて取得するようにした。予定が累積しすぎなければこれで対応可。

    if result == []:
        print("###新しく追加された課題はありませんでした###")
    else:
        print('###新しく追加された課題###')
        for report_title, class_name, deadline in result:
            print(report_title + "/" + class_name + ",提出期限:" + deadline)
    
    return "OK"


if __name__ == '__main__':
    main()