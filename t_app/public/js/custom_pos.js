frappe.provide("t_app.PointOfSale");

frappe.pages["point-of-sale"].on_page_load = function (wrapper) {
  // Load Tailwind CSS
  frappe.dom.add_css('/assets/t_app/css/output.css');

  frappe.ui.make_app_page({
    parent: wrapper,
    title: __("Point of Sale"),
    single_column: true,
  });

  frappe.require("point-of-sale.bundle.js", function () {
    wrapper.pos = new t_app.PointOfSale.Controller(wrapper);
    window.cur_pos = wrapper.pos;
    // Initialize main sections with Tailwind classes
    $(wrapper).find('.layout-main-section').append(`
      <div class="point-of-sale-app grid grid-cols-10 gap-md bg-gray-50 min-h-[45rem] h-[calc(100vh-200px)] max-h-[calc(100vh-200px)]">
        <div class="items-selector pos-card col-span-6 flex flex-col overflow-hidden">
          <div class="filter-section grid grid-cols-12 bg-fg p-lg pb-sm items-center">
            <div class="label col-span-4 pb-xs text-lg font-bold flex items-center">Items</div>
            <div class="search-field col-span-5 flex items-center mx-sm"></div>
            <div class="item-group-field col-span-3 flex items-center"></div>
          </div>
          <div class="items-container"></div>
        </div>
        <div class="customer-cart-container col-span-4 flex flex-col">
          <div class="customer-section pos-card flex flex-col p-md px-lg"></div>
          <div class="cart-container pos-card flex flex-col items-center mt-md relative h-full">
            <div class="abs-cart-container absolute flex flex-col p-lg w-full h-full">
              <div class="cart-label label pb-md">Cart</div>
              <div class="cart-items-section"></div>
            </div>
          </div>
        </div>
      </div>
    `);
  });
};

frappe.pages["point-of-sale"].refresh = function (wrapper) {
  if (document.scannerDetectionData) {
    onScan.detachFrom(document);
    wrapper.pos.wrapper.html("");
    wrapper.pos.check_opening_entry();
  }
};