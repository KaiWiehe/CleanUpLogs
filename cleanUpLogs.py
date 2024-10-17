import os
import sys
import datetime

# @Author: Kai.Wiehe


# Überprüfe, ob ein Log-Verzeichnis und die Anzahl der Tage als Parameter übergeben wurden
def get_parameters():
    if len(sys.argv) < 3:
        print(
            "Bitte gib den Pfad zu deinem Log-Verzeichnis und die Anzahl der Tage als Parameter an."
        )
        print(
            f"Verwendung: {sys.argv[0]} /pfad/zu/deinem/log ANZAHL_TAGE [GESCHÜTZTE_LISTE]"
        )
        print(
            f'Beispiel: {sys.argv[0]} /opt/wildfly-31.0.1.Final-0/standalone/log/ 14 "test_log_3.log.20222" "YatuWebClient/"'
        )
        sys.exit(1)
    log_dir = sys.argv[1]
    retention_days = int(sys.argv[2])
    protected_items = sys.argv[3:] if len(sys.argv) > 3 else []
    return log_dir, retention_days, protected_items


# Überprüfe, ob das angegebene Verzeichnis existiert
def verify_directory_exists(directory):
    if not os.path.isdir(directory):
        print(f"Das angegebene Verzeichnis existiert nicht: {directory}")
        sys.exit(1)


# Überprüfe, ob die Datei die Kriterien für das Löschen erfüllt
def should_delete_file(file, root, protected_items):
    # Überprüfe, ob die Datei oder das Verzeichnis geschützt ist
    if any(
        os.path.basename(file) == protected_item or protected_item in root
        for protected_item in protected_items
    ):
        return False
    if ".log" in file:
        suffix = file.split(".log", 1)[-1]
        return len(suffix) >= 2
    return False


# Lösche alle Log-Dateien, die älter als die festgelegte Aufbewahrungsfrist sind
def delete_old_files(directory, retention_days, protected_items):
    retention_time = datetime.datetime.now() - datetime.timedelta(days=retention_days)
    deleted_files = []

    for root, dirs, files in os.walk(directory):
        # Beschränke die Suche auf das Verzeichnis und die erste Ebene von Unterverzeichnissen
        if root == directory:
            # Bearbeite nur das aktuelle Verzeichnis und die direkten Unterverzeichnisse
            dirs[:] = [
                d
                for d in dirs
                if os.path.join(root, d).count(os.sep) - directory.count(os.sep) <= 1
            ]
        else:
            # Entferne tiefere Unterverzeichnisse
            dirs[:] = []

        for file in files:
            if should_delete_file(file, root, protected_items):
                file_path = os.path.join(root, file)
                file_mtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                )
                if file_mtime < retention_time:
                    os.remove(file_path)
                    deleted_files.append(file_path)

    return deleted_files


# Ausgabe der Ergebnisse
def print_deletion_summary(deleted_files):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if deleted_files:
        count = len(deleted_files)
        deleted_files_str = ", ".join(deleted_files)
        print(f"{current_date} -> {count} Dateien wurden gelöscht: {deleted_files_str}")
    else:
        print(f"{current_date} -> Keine Dateien wurden gelöscht.")


# Hauptprogramm
if __name__ == "__main__":
    LOG_DIR, LOG_RETENTION_DAYS, PROTECTED_ITEMS = get_parameters()
    verify_directory_exists(LOG_DIR)
    deleted_files = delete_old_files(LOG_DIR, LOG_RETENTION_DAYS, PROTECTED_ITEMS)
    print_deletion_summary(deleted_files)


# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_1.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_2.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_3.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_4.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_5.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_6.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_7.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_8.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_9.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/test_log_10.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_1.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_2.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_3.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_4.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_5.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_6.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_7.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_8.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_9.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test_log_10.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_1.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_2.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_3.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_4.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_5.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_6.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_7.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_8.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_9.log.20222
# touch -t $(date -d '20 days ago' +%Y%m%d%H%M) /opt/wildfly-31.0.1.Final-0/standalone/log/YatuWebClient/test/test_log_10.log.20222

# Alle zwei Tage um Mitternacht auszuführen
# 0 0 */2 * * python3 /opt/scripts/cleanUpLogs.py "/opt/wildfly-31.0.1.Final-0/standalone/log" 14 "server.log" "audit.log" "yatuWebClient.log" >> /opt/scripts/cleanUpLogs.log 2>&1
