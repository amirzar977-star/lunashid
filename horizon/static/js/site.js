/* ==========================================================================
   Horizon Properties — site behaviour
   Vanilla ES2017+, no dependencies. Everything is progressive enhancement:
   every control works without JavaScript except favourites, which are stored
   on the device.
   ========================================================================== */
(function () {
  'use strict';

  var SAVED_KEY = 'horizon:saved';

  function $(selector, scope) { return (scope || document).querySelector(selector); }
  function $$(selector, scope) {
    return Array.prototype.slice.call((scope || document).querySelectorAll(selector));
  }

  /* ---------------------------------------------------------------- header */
  function initHeader() {
    var header = $('[data-header]');
    var toggle = $('[data-nav-toggle]');
    var panel = $('[data-mobile-nav]');

    if (header) {
      var onScroll = function () {
        header.classList.toggle('is-scrolled', window.scrollY > 24);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('pageshow', onScroll);

      // Watching a sentinel keeps the header correct even when the scroll
      // position changes without a scroll event (viewport resize, restoration).
      var sentinel = $('[data-header-sentinel]');
      if (sentinel && 'IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          header.classList.toggle('is-scrolled', !entries[0].isIntersecting);
        }, { threshold: 0 }).observe(sentinel);
      }
    }

    if (!toggle || !panel) { return; }

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      panel.classList.toggle('is-open', open);
      panel.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('nav-open', open);
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    panel.addEventListener('click', function (event) {
      if (event.target.closest('a')) { setOpen(false); }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { setOpen(false); }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024) { setOpen(false); }
    });
  }

  /* ---------------------------------------------------------------- reveal */
  function initReveal() {
    var items = $$('.reveal');
    if (!items.length) { return; }

    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(function (item) { item.classList.add('is-visible'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });

    items.forEach(function (item) { observer.observe(item); });

    // Safety net: anything already on screen when the page settles becomes visible.
    window.setTimeout(function () {
      items.forEach(function (item) {
        var rect = item.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          item.classList.add('is-visible');
        }
      });
    }, 1400);
  }

  /* -------------------------------------------------------------- carousel */
  function initCarousel() {
    $$('[data-carousel]').forEach(function (root) {
      var track = $('[data-carousel-track]', root);
      if (!track) { return; }
      var prev = $('[data-carousel-prev]', root);
      var next = $('[data-carousel-next]', root);

      function step() {
        var card = track.querySelector('.property-card');
        if (!card) { return Math.round(track.clientWidth * 0.8); }
        var styles = window.getComputedStyle(track);
        var gap = parseFloat(styles.columnGap || styles.gap || '24') || 24;
        return card.getBoundingClientRect().width + gap;
      }

      function goForward() {
        var atEnd = track.scrollLeft + track.clientWidth + 8 >= track.scrollWidth;
        track.scrollTo({ left: atEnd ? 0 : track.scrollLeft + step(), behavior: 'smooth' });
      }

      function goBack() {
        if (track.scrollLeft <= 8) {
          track.scrollTo({ left: track.scrollWidth, behavior: 'smooth' });
          return;
        }
        track.scrollTo({ left: track.scrollLeft - step(), behavior: 'smooth' });
      }

      if (next) { next.addEventListener('click', goForward); }
      if (prev) { prev.addEventListener('click', goBack); }

      track.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowRight') { event.preventDefault(); goForward(); }
        if (event.key === 'ArrowLeft') { event.preventDefault(); goBack(); }
      });

      // Pointer drag on desktop; touch devices keep native momentum scrolling.
      var dragging = false;
      var startX = 0;
      var startScroll = 0;
      var moved = false;

      track.addEventListener('pointerdown', function (event) {
        if (event.pointerType === 'touch' || event.button !== 0) { return; }
        dragging = true;
        moved = false;
        startX = event.clientX;
        startScroll = track.scrollLeft;
        track.classList.add('is-dragging');
        if (track.setPointerCapture) { track.setPointerCapture(event.pointerId); }
      });

      track.addEventListener('pointermove', function (event) {
        if (!dragging) { return; }
        var delta = event.clientX - startX;
        if (Math.abs(delta) > 4) { moved = true; }
        track.scrollLeft = startScroll - delta;
      });

      function endDrag(event) {
        if (!dragging) { return; }
        dragging = false;
        track.classList.remove('is-dragging');
        if (event && track.releasePointerCapture && event.pointerId != null &&
            track.hasPointerCapture && track.hasPointerCapture(event.pointerId)) {
          track.releasePointerCapture(event.pointerId);
        }
      }

      track.addEventListener('pointerup', endDrag);
      track.addEventListener('pointercancel', endDrag);
      track.addEventListener('pointerleave', endDrag);
      track.addEventListener('click', function (event) {
        if (moved) { event.preventDefault(); event.stopPropagation(); moved = false; }
      }, true);
    });
  }

  /* --------------------------------------------------------------- filters */
  function initFilters() {
    var form = $('[data-filters]');
    if (!form) { return; }

    $$('[data-filter-select]', form).forEach(function (select) {
      select.addEventListener('change', function () { form.submit(); });
    });

    var search = $('[data-filter-search]', form);
    var timer = null;
    if (search) {
      search.addEventListener('input', function () {
        window.clearTimeout(timer);
        timer = window.setTimeout(function () { form.submit(); }, 450);
      });
      search.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') { event.preventDefault(); form.submit(); }
      });
    }

    var toggle = $('[data-filters-toggle]', form);
    var panel = $('[data-filters-panel]', form);
    if (toggle && panel) {
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        panel.classList.toggle('is-open', !open);
      });
    }
  }

  /* ------------------------------------------------- gallery + lightbox --- */
  function initGallery() {
    var gallery = $('[data-gallery]');
    if (!gallery) { return; }

    var main = $('[data-gallery-main]', gallery);
    var thumbs = $$('[data-gallery-thumb]', gallery);
    var lightbox = $('[data-lightbox]');
    var lightboxImage = lightbox ? $('[data-lightbox-image]', lightbox) : null;
    var lightboxCount = lightbox ? $('[data-lightbox-count]', lightbox) : null;
    var index = 0;

    function current() { return thumbs[index] || null; }

    function updateViewer() {
      var thumb = current();
      if (!thumb || !lightboxImage) { return; }
      lightboxImage.src = thumb.dataset.src;
      lightboxImage.alt = thumb.dataset.alt || '';
      if (lightboxCount) { lightboxCount.textContent = (index + 1) + ' / ' + thumbs.length; }
    }

    function show(next) {
      if (!thumbs.length) { return; }
      index = (next + thumbs.length) % thumbs.length;
      var thumb = current();
      if (main) {
        main.src = thumb.dataset.src;
        main.alt = thumb.dataset.alt || main.alt;
      }
      thumbs.forEach(function (item, i) {
        var active = i === index;
        item.classList.toggle('is-active', active);
        if (active) { item.setAttribute('aria-current', 'true'); }
        else { item.removeAttribute('aria-current'); }
      });
      updateViewer();
    }

    thumbs.forEach(function (thumb, i) {
      thumb.addEventListener('click', function () { show(i); });
    });

    var openBtn = $('[data-gallery-open]', gallery);
    if (openBtn && lightbox && typeof lightbox.showModal === 'function') {
      openBtn.addEventListener('click', function () {
        show(index);
        lightbox.showModal();
      });
    }

    if (!lightbox) { return; }

    $$('[data-lightbox-close]', lightbox).forEach(function (btn) {
      btn.addEventListener('click', function () { lightbox.close(); });
    });
    var prevBtn = $('[data-lightbox-prev]', lightbox);
    var nextBtn = $('[data-lightbox-next]', lightbox);
    if (prevBtn) { prevBtn.addEventListener('click', function () { show(index - 1); }); }
    if (nextBtn) { nextBtn.addEventListener('click', function () { show(index + 1); }); }

    lightbox.addEventListener('click', function (event) {
      if (event.target === lightbox) { lightbox.close(); }
    });
    lightbox.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowRight') { show(index + 1); }
      if (event.key === 'ArrowLeft') { show(index - 1); }
    });
  }

  /* ----------------------------------------------------------- enquiry modal */
  function initInquiry() {
    var modal = $('[data-inquiry-modal]');
    if (!modal || typeof modal.showModal !== 'function') { return; }

    var title = $('[data-modal-title]', modal);
    var sub = $('[data-modal-sub]', modal);
    var eyebrow = $('[data-modal-eyebrow]', modal);
    var context = $('[data-modal-context]', modal);
    var when = $('[data-modal-when]', modal);
    var propertyField = $('[data-modal-property]', modal);
    var intentField = $('[data-modal-intent]', modal);
    var form = $('[data-inquiry-form]', modal);
    var success = $('[data-modal-success]', modal);
    var successText = $('[data-modal-success-text]', modal);

    $$('[data-open-inquiry]').forEach(function (button) {
      button.addEventListener('click', function () {
        var intent = button.dataset.openInquiry || 'viewing';
        var isViewing = intent === 'viewing';
        var propertyName = button.dataset.propertyName || '';

        if (intentField) { intentField.value = intent; }
        if (propertyField) { propertyField.value = button.dataset.property || ''; }
        if (title) { title.textContent = isViewing ? 'Schedule a viewing' : 'Contact the listing advisor'; }
        if (sub) {
          sub.textContent = isViewing
            ? 'Tell us when suits you and an advisor will confirm the time by email.'
            : 'Ask anything about this property — the listing advisor replies personally.';
        }
        if (eyebrow) { eyebrow.textContent = isViewing ? 'Viewing request' : 'Property enquiry'; }
        if (context) {
          context.textContent = propertyName;
          context.hidden = !propertyName;
        }
        if (when) { when.hidden = !isViewing; }
        if (form) {
          form.hidden = false;
          clearFieldErrors(form);
          var errorBox = $('[data-form-error]', form);
          if (errorBox) { errorBox.hidden = true; }
        }
        if (success) { success.hidden = true; }

        modal.showModal();
      });
    });

    $$('[data-modal-close]', modal).forEach(function (button) {
      button.addEventListener('click', function () { modal.close(); });
    });

    modal.addEventListener('click', function (event) {
      if (event.target === modal) { modal.close(); }
    });
  }

  /* ------------------------------------------------------------- ajax forms */
  function clearFieldErrors(form) {
    $$('.field.has-error', form).forEach(function (field) {
      field.classList.remove('has-error');
      var message = $('.field-error', field);
      if (message) { message.remove(); }
    });
    var errorBox = $('[data-form-error]', form);
    if (errorBox) { errorBox.hidden = true; }
  }

  function markFieldError(form, name, message) {
    var input = form.querySelector('[name="' + name + '"]');
    if (!input) { return; }
    var field = input.closest('.field');
    if (!field) { return; }
    field.classList.add('has-error');
    var note = document.createElement('p');
    note.className = 'field-error';
    note.textContent = message;
    field.appendChild(note);
    if (!form.dataset.focusSet) {
      form.dataset.focusSet = '1';
      input.focus();
    }
  }

  function initAjaxForms() {
    $$('[data-ajax-form]').forEach(function (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        delete form.dataset.focusSet;

        var endpoint = form.dataset.endpoint;
        if (!endpoint) { return; }

        var submit = $('[data-submit]', form) || form.querySelector('button[type="submit"]');
        var original = submit ? submit.innerHTML : '';
        var note = $('[data-form-note]', form);
        var errorBox = $('[data-form-error]', form);

        clearFieldErrors(form);
        if (note) { note.textContent = ''; note.classList.remove('is-success'); }
        if (submit) {
          submit.setAttribute('aria-busy', 'true');
          submit.disabled = true;
          submit.innerHTML = 'Sending…';
        }

        fetch(endpoint, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'fetch' },
          body: new FormData(form)
        })
          .then(function (response) {
            return response.json().catch(function () { return {}; }).then(function (data) {
              return { ok: response.ok, data: data };
            });
          })
          .then(function (result) {
            if (!result.ok || !result.data.ok) {
              var errors = result.data.errors || {};
              var names = Object.keys(errors);
              if (names.length) {
                names.forEach(function (name) { markFieldError(form, name, errors[name]); });
                if (errorBox) {
                  errorBox.textContent = 'Please check the highlighted fields and try again.';
                  errorBox.hidden = false;
                }
              } else if (errorBox) {
                errorBox.textContent = 'Something went wrong — please try again, or call the office on (555) 246-7890.';
                errorBox.hidden = false;
              }
              return;
            }

            if (form.hasAttribute('data-inquiry-form')) {
              var modal = form.closest('[data-inquiry-modal]');
              var success = modal ? $('[data-modal-success]', modal) : null;
              var successText = modal ? $('[data-modal-success-text]', modal) : null;
              form.reset();
              form.hidden = true;
              if (successText) { successText.textContent = result.data.message || 'Thank you — we will be in touch.'; }
              if (success) { success.hidden = false; }
              return;
            }

            form.reset();
            if (note) {
              note.textContent = result.data.message || 'Thank you — we will be in touch.';
              note.classList.add('is-success');
            }
          })
          .catch(function () {
            if (errorBox) {
              errorBox.textContent = 'We could not reach the server. Please check your connection and try again.';
              errorBox.hidden = false;
            }
          })
          .then(function () {
            if (submit) {
              submit.removeAttribute('aria-busy');
              submit.disabled = false;
              submit.innerHTML = original;
            }
          });
      });
    });
  }

  /* ------------------------------------------------------------ favourites */
  function readSaved() {
    try {
      var raw = window.localStorage.getItem(SAVED_KEY);
      var list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list : [];
    } catch (error) {
      return [];
    }
  }

  function writeSaved(list) {
    try { window.localStorage.setItem(SAVED_KEY, JSON.stringify(list)); } catch (error) { /* storage unavailable */ }
  }

  function hasSaved(slug) {
    return readSaved().indexOf(slug) !== -1;
  }

  function syncFavourites() {
    var list = readSaved();

    $$('[data-favorite]').forEach(function (button) {
      var on = list.indexOf(button.dataset.favorite) !== -1;
      button.setAttribute('aria-pressed', String(on));
      var label = $('[data-favorite-label]', button);
      if (label) { label.textContent = on ? 'Saved to your shortlist' : 'Save this property'; }
    });

    var counters = $$('[data-saved-count]');
    counters.forEach(function (counter) {
      counter.hidden = list.length === 0;
      counter.textContent = String(list.length);
    });

    var grid = $('[data-saved-grid]');
    if (grid) {
      var visible = 0;
      $$('[data-slug]', grid).forEach(function (card) {
        var on = list.indexOf(card.dataset.slug) !== -1;
        card.hidden = !on;
        if (on) { visible += 1; }
      });
      grid.hidden = visible === 0;

      var empty = $('[data-saved-empty]');
      if (empty) { empty.hidden = visible !== 0; }

      var summary = $('[data-saved-summary]');
      if (summary) {
        summary.textContent = visible
          ? visible + (visible === 1 ? ' property saved' : ' properties saved') + ' on this device.'
          : 'Properties you save while browsing appear here. Your shortlist stays on this device.';
      }
    }
  }

  function initFavourites() {
    syncFavourites();

    document.addEventListener('click', function (event) {
      var button = event.target.closest('[data-favorite]');
      if (!button) { return; }
      event.preventDefault();
      var slug = button.dataset.favorite;
      if (!slug) { return; }
      var list = readSaved();
      var position = list.indexOf(slug);
      if (position === -1) { list.push(slug); } else { list.splice(position, 1); }
      writeSaved(list);
      syncFavourites();
    });

    window.addEventListener('storage', function (event) {
      if (event.key === SAVED_KEY) { syncFavourites(); }
    });
  }

  /* ---------------------------------------------------------------- notices */
  function initFlash() {
    $$('[data-flash-stack] .flash').forEach(function (flash, i) {
      window.setTimeout(function () { flash.classList.add('is-hidden'); }, 5000 + i * 400);
    });
  }

  /* ------------------------------------------------------------------ init */
  function init() {
    initHeader();
    initReveal();
    initCarousel();
    initFilters();
    initGallery();
    initInquiry();
    initAjaxForms();
    initFavourites();
    initFlash();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
