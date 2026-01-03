# Transfer Checklist

## Files to Transfer

- [ ] bitcoin-27.0-x86_64-linux-gnu.tar.gz (~26 MB)
- [ ] install_bitcoin.sh (installation script)
- [ ] OFFLINE_INSTALLATION_INSTRUCTIONS.md (this guide)

## Transfer Methods

### USB Drive
- [ ] Copy files to USB
- [ ] Safely eject USB
- [ ] Transfer to restricted machine
- [ ] Verify file integrity (check file size)

### Network Share
- [ ] Copy to shared drive
- [ ] Access from restricted machine
- [ ] Copy to local directory
- [ ] Verify file integrity

### SCP/SFTP
- [ ] Verify internal network access
- [ ] Use scp or sftp to transfer
- [ ] Verify transfer completed
- [ ] Check file permissions

## After Transfer

- [ ] Verify file size matches
- [ ] Check SHA256 if possible
- [ ] Make install script executable
- [ ] Run installation
- [ ] Test bitcoind --version

## Notes

File size: bitcoin-27.0-x86_64-linux-gnu.tar.gz should be ~26 MB
If size differs significantly, re-transfer the file.
