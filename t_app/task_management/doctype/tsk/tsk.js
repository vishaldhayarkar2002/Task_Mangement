

frappe.ui.form.on('tsk', {
    refresh: function(frm) {
        if (frm.doc.status === "Completed") {
            frappe.msgprint("🎉 Task Completed!");
        }
       
        if (frm.doc.status !== 'Completed') {
            frm.add_custom_button('Mark as In Progress', () => {
                frm.set_value('status', 'In progress');
                frm.save();
            });

            frm.add_custom_button('Mark as Completed', () => {
                frm.set_value('status', 'Completed');
                frm.save();
            });
        }
    },

    setup: function(frm) {
        
        if (frm.is_new()) {
            frm.set_value('status', 'Open');
        }
    },
    status: function(frm) {
        if (frm.doc.status === "Completed") {
            frappe.msgprint("✅ Task marked as Completed!");
        }
    },
    priority: function(frm) {
        if (frm.doc.priority === "High") {
            frm.set_value("status", "In Progress");
            frm.refresh_field("status");  // Force refresh to reflect the change
        }
    }, 
    e_date: function(frm) {
        if (frm.doc.e_date < frappe.datetime.get_today()) {
            frappe.msgprint("⚠️ End Date is in the past. Please update it.");
        }
    },
    s_date: function(frm) {
        if (frm.doc.s_date < frappe.datetime.get_today()) {
            frappe.msgprint("⚠️ Start Date is in the past. Please update it.");
        }
    }
});


