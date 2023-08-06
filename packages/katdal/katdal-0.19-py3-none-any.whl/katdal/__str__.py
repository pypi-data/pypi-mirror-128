    def __str__(self):
        """Verbose human-friendly string representation of data set."""
        # Start with static file information
        observer = self.observer if self.observer else '-'
        experiment_id = self.experiment_id if self.experiment_id else '-'
        description = self.description if self.description else 'No description'
        dump_rate = 1 / self.dump_period
        # Summary of subarrays
        for n, sub in enumerate(self.subarrays):
            ant_names = ','.join([ant.name for ant in sub.ants])
            descr += '  {:2d}  {:>28}  {:2d}      {:3d}\n'.format(
                     n, ant_names.ljust(7 * 4 + 6), len(sub.inputs), len(sub.corr_products))


        descr = f"""
===============================================================================
Name: {self.name} (version {self.version})
===============================================================================
Observer: {observer}  Experiment ID: {experiment_id}
Description: '{description}'
Observed from {self.start_time.local()} to {self.end_time.local()}
Dump rate / period: {dump_rate:.5f} Hz / {self.dump_period:.3f} s
Subarrays: {len(self.subarrays)}
  ID  Antennas                            Inputs  Corrprods
"""

        descr += f""""
Spectral Windows: {len(self.spectral_windows)}
  ID Band Product  CentreFreq(MHz)  Bandwidth(MHz)  Channels  ChannelWidth(kHz)
"""
        for n, spw in enumerate(self.spectral_windows):
            descr += '{:4d} {:4} {:9} {:9.3f}        {:8.3f}          {:5d}     {:9.3f}\n'.format(
                     n, spw.band if spw.band else '-', spw.product if spw.product else '-',
                     spw.centre_freq / 1e6, spw.channel_width / 1e6 * spw.num_chans,
                     spw.num_chans, spw.channel_width / 1e3)

        # Now add dynamic information, which depends on the current selection criteria
        descr += """
-------------------------------------------------------------------------------
Data selected according to the following criteria:
"""
        for k, v in sorted(self._selection.items()):
            descr.append('  {}={}'.format(k, f"'{v}'" if isinstance(v, str) else v))
        descr.append('-------------------------------------------------------------------------------')
        descr.append('Shape: (%d dumps, %d channels, %d correlation products) => Size: %s' %
                     tuple(list(self.shape) + ['%.3f %s' % ((self.size / 1e9, 'GB') if self.size > 1e9 else
                                                            (self.size / 1e6, 'MB') if self.size > 1e6 else
                                                            (self.size / 1e3, 'KB'))]))
        autocorrs = np.array([(inpA[:-1] == inpB[:-1]) for inpA, inpB in self.corr_products])
        crosscorrs = np.array([(inpA[:-1] != inpB[:-1]) for inpA, inpB in self.corr_products])
        descr.append('Antennas: %s  Inputs: %d  Autocorr: %s  Crosscorr: %s' %
                     (','.join([('*' + ant.name if ant.name == self.ref_ant else ant.name) for ant in self.ants]),
                      len(self.inputs), 'yes' if np.any(autocorrs) else 'no', 'yes' if np.any(crosscorrs) else 'no'))
        chan_min, chan_max = self.channels.argmin(), self.channels.argmax()
        descr.append('Channels: %d (index %d - %d, %8.3f MHz - %8.3f MHz), each %7.3f kHz wide' %
                     (len(self.channels), self.channels[chan_min], self.channels[chan_max],
                      self.freqs[chan_min] / 1e6, self.freqs[chan_max] / 1e6, self.channel_width / 1e3))
        # Discover maximum name and tag string lengths for targets beforehand
        name_len, tag_len = 4, 4
        for n in self.target_indices:
            target = self.catalogue.targets[n]
            name_len = max(len(target.name), name_len)
            tag_len = max(len(' '.join(target.tags[1:] if target.body_type != 'xephem' else target.tags[2:])), tag_len)
        descr += ['Targets: %d selected out of %d in catalogue' % (len(self.target_indices), len(self.catalogue)),
                  '  ID  %s  Type      RA(J2000)     DEC(J2000)  %s  Dumps  ModelFlux(Jy)' %
                  ('Name'.ljust(name_len), 'Tags'.ljust(tag_len))]
        for n in self.target_indices:
            target = self.catalogue.targets[n]
            target_type = target.body_type if target.body_type != 'xephem' else target.tags[1]
            tags = ' '.join(target.tags[1:] if target.body_type != 'xephem' else target.tags[2:])
            ra, dec = target.radec() if target_type == 'radec' else ('-', '-')
            # Calculate average target flux over selected frequency band
            flux_spectrum = target.flux_density(self.freqs / 1e6)
            flux_valid = ~np.isnan(flux_spectrum)
            flux = '{:9.2f}'.format(flux_spectrum[flux_valid].mean()) if np.any(flux_valid) else ''
            target_dumps = ((self.sensor.get('Observation/target_index') == n) & self._time_keep).sum()
            descr.append('  %2d  %s  %s  %11s  %11s  %s  %5d  %s' %
                         (n, target.name.ljust(name_len), target_type.ljust(8),
                          ra, dec, tags.ljust(tag_len), target_dumps, flux))
        scans = self.sensor.get('Observation/scan_index')
        compscans = self.sensor.get('Observation/compscan_index')
        total_scans, total_compscans = len(scans.unique_values), len(compscans.unique_values)
        descr += ['Scans: %d selected out of %d total       Compscans: %d selected out of %d total' %
                  (len(self.scan_indices), total_scans, len(self.compscan_indices), total_compscans),
                  '  Date        Timerange(UTC)       ScanState  CompScanLabel  Dumps  Target']
        current_date = ''
        for scan, state, target in self.scans():
            start, end = time.gmtime(self.timestamps[0]), time.gmtime(self.timestamps[-1])
            start_date, start_time = time.strftime('%d-%b-%Y/', start), time.strftime('%H:%M:%S', start)
            end_date, end_time = time.strftime('%d-%b-%Y/', end), time.strftime('%H:%M:%S', end)
            timerange = (start_date if start_date != current_date else '') + start_time
            current_date = start_date
            timerange += ' - ' + (end_date if end_date != current_date else '') + end_time
            compscan, label = self.sensor['Observation/compscan_index'][0], self.sensor['Observation/label'][0]
            descr.append('  %31s  %3d:%5s  %3d:%9s  %5d  %3d:%s' %
                         (timerange, scan, state.ljust(5), compscan, label.ljust(9),
                          self.shape[0], self.target_indices[0], target.name))
        return '\n'.join(descr)




      .1.3.56789|0123..6789|......678.
      .1.3.56.89|0123456789|......678.
      .1.3

"""
m00#      |m01#      |m02#
-1-3-56789|0123--6789|------678-
-1-3-56-89|0123456789|--23--678-
-1-3
"""
"""
m000-m029|.1.3.56789|0123..6789|......678.
m030-m059|.1.3.56.89|0123456789|..23..678.
m060-m063|.1.3
"""

"""
m000-m029|.1.3.56789|0123..6789|......678.|
m030-m063|.1.3.56.89|0123456789|..23..678.|.1.3
"""
"""
m000-m029|_1_3_56789|0123__6789|______678_|
m030-m063|_1_3_56_89|0123456789|__23__678_|_1_3
"""
m
0
0
.
1
.
3
.
5
6
7
8
9
