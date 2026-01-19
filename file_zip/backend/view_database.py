#!/usr/bin/env python3
"""
UIC Patent Portal - Database Viewer
Simple script to view database contents with user_id support
"""

import sqlite3
import json
from datetime import datetime

def view_database():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        print("\n╔" + "=" * 58 + "╗")
        print("║" + "  🗄️  UIC Patent Portal - Database Contents  ".center(58) + "║")
        print("╚" + "=" * 58 + "╝\n")
        
        # Users
        cur.execute("SELECT COUNT(*) as count FROM users")
        user_count = cur.fetchone()['count']
        print(f"👤 Total Registered Users: {user_count}")
        
        if user_count > 0:
            print("\n   Recent Users:")
            cur.execute("""
                SELECT user_id, name, email, user_type, registration_date 
                FROM users 
                ORDER BY registration_date DESC 
                LIMIT 5
            """)
            
            users = cur.fetchall()
            for user in users:
                date = datetime.fromisoformat(user['registration_date']).strftime('%Y-%m-%d %H:%M')
                print(f"   • {user['user_id']} - {user['name']} ({user['user_type']})")
                print(f"     Email: {user['email']}")
                print(f"     Registered: {date}\n")
        
        # Applications
        cur.execute("SELECT COUNT(*) as count FROM applications")
        app_count = cur.fetchone()['count']
        print(f"\n📋 Total Applications: {app_count}")
        
        if app_count > 0:
            print("\n   Recent Applications:")
            cur.execute("""
                SELECT application_id, user_id, name, patent_title, submission_date 
                FROM applications 
                ORDER BY submission_date DESC 
                LIMIT 5
            """)
            
            applications = cur.fetchall()
            for app in applications:
                date = datetime.fromisoformat(app['submission_date']).strftime('%Y-%m-%d %H:%M')
                print(f"   • {app['application_id']}")
                print(f"     User: {app['user_id']} - {app['name']}")
                print(f"     Title: {app['patent_title']}")
                print(f"     Date: {date}\n")
        
        # Team Members
        cur.execute("SELECT COUNT(*) as count FROM team_members")
        member_count = cur.fetchone()['count']
        print(f"\n👥 Total Team Members: {member_count}")
        
        # Files
        cur.execute("SELECT COUNT(*) as count FROM files")
        file_count = cur.fetchone()['count']
        print(f"📎 Total Files Uploaded: {file_count}")
        
        # Statistics by status
        print("\n📊 Applications by Status:")
        cur.execute("""
            SELECT status, COUNT(*) as count 
            FROM applications 
            GROUP BY status 
            ORDER BY count DESC
        """)
        status_stats = cur.fetchall()
        
        if status_stats:
            for status in status_stats:
                status_name = status['status'].title() if status['status'] else "Unknown"
                print(f"   • {status_name}: {status['count']}")
        else:
            print("   No status data available")
        
        # Statistics by department
        print("\n📊 Applications by Department:")
        cur.execute("""
            SELECT department, COUNT(*) as count 
            FROM applications 
            WHERE department IS NOT NULL AND department != ''
            GROUP BY department 
            ORDER BY count DESC
        """)
        
        dept_stats = cur.fetchall()
        if dept_stats:
            for dept in dept_stats:
                print(f"   • {dept['department']}: {dept['count']}")
        else:
            print("   No department data available")
        
        # Statistics by applicant type
        print("\n👤 Applications by Type:")
        cur.execute("""
            SELECT applicant_type, COUNT(*) as count 
            FROM applications 
            WHERE applicant_type IS NOT NULL AND applicant_type != ''
            GROUP BY applicant_type 
            ORDER BY count DESC
        """)
        
        type_stats = cur.fetchall()
        if type_stats:
            for type_stat in type_stats:
                print(f"   • {type_stat['applicant_type']}: {type_stat['count']}")
        else:
            print("   No applicant type data available")
        
        # Statistics by patent type
        print("\n🔬 Applications by Patent Type:")
        cur.execute("""
            SELECT patent_type, COUNT(*) as count 
            FROM applications 
            WHERE patent_type IS NOT NULL AND patent_type != ''
            GROUP BY patent_type 
            ORDER BY count DESC
        """)
        
        patent_stats = cur.fetchall()
        if patent_stats:
            for patent_stat in patent_stats:
                print(f"   • {patent_stat['patent_type']}: {patent_stat['count']}")
        else:
            print("   No patent type data available")
        
        # User type distribution
        print("\n🎓 Users by Type:")
        cur.execute("""
            SELECT user_type, COUNT(*) as count 
            FROM users 
            WHERE user_type IS NOT NULL AND user_type != ''
            GROUP BY user_type 
            ORDER BY count DESC
        """)
        
        user_type_stats = cur.fetchall()
        if user_type_stats:
            for user_stat in user_type_stats:
                print(f"   • {user_stat['user_type']}: {user_stat['count']}")
        else:
            print("   No user type data available")
        
        # Applications per user
        print("\n📈 Top Users by Applications:")
        cur.execute("""
            SELECT a.user_id, COUNT(*) as app_count, u.name, u.email
            FROM applications a
            LEFT JOIN users u ON a.user_id = u.user_id
            GROUP BY a.user_id
            ORDER BY app_count DESC
            LIMIT 5
        """)
        
        top_users = cur.fetchall()
        if top_users:
            for user in top_users:
                print(f"   • {user['user_id']} ({user['name']}): {user['app_count']} applications")
        
        print("\n" + "=" * 60)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_application_details(app_id):
    """View detailed information for a specific application"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Get application details
        cur.execute("SELECT * FROM applications WHERE application_id = ?", (app_id,))
        app = cur.fetchone()
        
        if not app:
            print(f"❌ Application {app_id} not found")
            return
        
        # Get user details
        user_info = ""
        if app['user_id']:
            cur.execute("SELECT * FROM users WHERE user_id = ?", (app['user_id'],))
            user = cur.fetchone()
            if user:
                user_info = f"\n👤 User Details:\n   ID: {user['user_id']}\n   Type: {user['user_type']}\n   Registered: {user['registration_date']}"
        
        print(f"\n╔" + "=" * 58 + "╗")
        print("║" + f"  📋 Application Details: {app_id}  ".center(58) + "║")
        print("╚" + "=" * 58 + "╝\n")
        
        print(f"📌 Application ID: {app['application_id']}")
        print(f"👤 User ID: {app['user_id']}")
        print(f"📝 Name: {app['name']}")
        print(f"📧 Email: {app['email']}")
        print(f"🏢 Department: {app['department']}")
        print(f"🌍 Branch: {app['branch']}")
        print(f"📋 Applicant Type: {app['applicant_type']}")
        print(f"📞 Contact: {app['contact']}")
        print(f"\n🔬 Patent Details:")
        print(f"   Title: {app['patent_title']}")
        print(f"   Type: {app['patent_type']}")
        print(f"   Description: {app['description']}")
        print(f"   Novelty: {app['novelty']}")
        print(f"   Submission Date: {app['submission_date']}")
        
        if user_info:
            print(user_info)
        
        # Get team members
        cur.execute("SELECT * FROM team_members WHERE application_id = ?", (app_id,))
        members = cur.fetchall()
        
        if members:
            print(f"\n👥 Team Members ({len(members)}):")
            for member in members:
                print(f"   • {member['member_name']} - {member['member_role']}")
                if member['member_department']:
                    print(f"     Department: {member['member_department']}")
                if member['member_email']:
                    print(f"     Email: {member['member_email']}")
        
        # Get files
        cur.execute("SELECT * FROM files WHERE application_id = ?", (app_id,))
        files = cur.fetchall()
        
        if files:
            print(f"\n📎 Uploaded Files ({len(files)}):")
            for file in files:
                print(f"   • {file['file_name']}")
                print(f"     Path: {file['file_path']}")
        
        print("\n" + "=" * 60 + "\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_user_details(user_id):
    """View detailed information for a specific user"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Get user details
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cur.fetchone()
        
        if not user:
            print(f"❌ User {user_id} not found")
            return
        
        print(f"\n╔" + "=" * 58 + "╗")
        print("║" + f"  👤 User Details: {user_id}  ".center(58) + "║")
        print("╚" + "=" * 58 + "╝\n")
        
        print(f"👤 User ID: {user['user_id']}")
        print(f"📝 Name: {user['name']}")
        print(f"📧 Email: {user['email']}")
        print(f"📋 Type: {user['user_type']}")
        print(f"🏢 Department: {user['department']}")
        print(f"🌍 Branch: {user['branch']}")
        print(f"📞 Contact: {user['contact']}")
        print(f"📅 Registration Date: {user['registration_date']}")
        print(f"✅ Active: {'Yes' if user['is_active'] else 'No'}")
        
        # Get user's applications
        cur.execute("""
            SELECT application_id, patent_title, submission_date 
            FROM applications 
            WHERE user_id = ? 
            ORDER BY submission_date DESC
        """, (user_id,))
        
        applications = cur.fetchall()
        
        if applications:
            print(f"\n📋 Applications ({len(applications)}):")
            for app in applications:
                date = datetime.fromisoformat(app['submission_date']).strftime('%Y-%m-%d %H:%M')
                print(f"   • {app['application_id']}")
                print(f"     Title: {app['patent_title']}")
                print(f"     Date: {date}")
        else:
            print(f"\n📋 Applications: No applications found")
        
        print("\n" + "=" * 60 + "\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def export_to_json(output_file='export.json'):
    """Export all database contents to JSON"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        data = {}
        
        # Export users
        cur.execute("SELECT * FROM users")
        data['users'] = [dict(row) for row in cur.fetchall()]
        
        # Export applications
        cur.execute("SELECT * FROM applications")
        data['applications'] = [dict(row) for row in cur.fetchall()]
        
        # Export team members
        cur.execute("SELECT * FROM team_members")
        data['team_members'] = [dict(row) for row in cur.fetchall()]
        
        # Export files
        cur.execute("SELECT * FROM files")
        data['files'] = [dict(row) for row in cur.fetchall()]
        
        # Write to JSON file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Database exported to {output_file}")
        print(f"   Users: {len(data['users'])}")
        print(f"   Applications: {len(data['applications'])}")
        print(f"   Team Members: {len(data['team_members'])}")
        print(f"   Files: {len(data['files'])}\n")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Export error: {e}")

def print_help():
    print("\n💡 Usage:")
    print("   python3 view_database.py                         # View overview")
    print("   python3 view_database.py app UIC-PAT-XXXXXXXX  # View specific application")
    print("   python3 view_database.py user UIC-USER-XXXXXXXX # View specific user")
    print("   python3 view_database.py export [filename.json] # Export to JSON\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "app" and len(sys.argv) > 2:
            # View specific application
            view_application_details(sys.argv[2])
        elif command == "user" and len(sys.argv) > 2:
            # View specific user
            view_user_details(sys.argv[2])
        elif command == "export":
            # Export to JSON
            output_file = sys.argv[2] if len(sys.argv) > 2 else 'export.json'
            export_to_json(output_file)
        else:
            print("❌ Invalid command")
            print_help()
    else:
        # View database overview
        view_database()
        print_help()

def print_help():
    print("\n💡 Usage:")
    print("   python3 view_database.py                         # View overview")
    print("   python3 view_database.py app UIC-PAT-XXXXXXXX  # View specific application")
    print("   python3 view_database.py user UIC-USER-XXXXXXXX # View specific user")
    print("   python3 view_database.py export [filename.json] # Export to JSON\n")